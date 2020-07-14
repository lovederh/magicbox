$(function () {
	//构造时间选择器
	laydate.render({ elem: '#weekup_time', type: 'time' });
	laydate.render({ elem: '#close_time', type: 'time' });
	//设置开关机使用的时间选择
	laydate.render({ elem: '#set_weekup_time', type: 'time' });
	laydate.render({ elem: '#set_close_time', type: 'time' });

	//确定表格高度
	var gridHeight = $(document).height() - 178;//减的越少列表越高
	//初始化表格
	$('#js_jqGrid').jqGrid({
		url: '/base/terminal/equ_query',
	    datatype: "json",
	    colModel: [
	       	{ label: 'id', name: 'id', hidden: true, key: true },
	    	{ label: 'mac地址', name: 'mac', width: 100 },
	    	{ label: '设备名称', name: 'equ_name', width: 100 },
			{ label: '设备别名', name: 'alias_name', width: 50 },
	    	{ label: '终端类型', name: 'equ_type', width: 50, formatter: function(value, options, row){
				if('ps' == value) {
					return '画屏';
				} else if('ytj' == value) {
					return '一体机';
				}
				return '';
			}},
	    	{ label: '开机时间', name: 'weekup_time', width: 100 },
			{ label: '关机时间', name: 'close_time', width: 100 },
			{ label: '操作', name: 'operate', sortable: false, width: 100, formatter: function(cellValue, options, rowObject) {
	        	var operateBtn =
					'<a class="btn btn-sm btn-success" href=\'javascript:editFunc("' + rowObject.id + '");\' >修改</a> ' +
	    			'<a class="btn btn-sm btn-danger" href=\'javascript:delFunc("' + rowObject.id + '");\' >删除</a> ' +
					'<a class="btn btn-sm btn-success" href=\'javascript:viewFunc("' + rowObject.id + '");\' >详情</a>';
	            return operateBtn;
	        }}
	    ],
		viewrecords: true,
	    height: gridHeight,
	    rowNum: 10,
		rowList : [10, 20, 50, 80, 100],
	    autowidth: true,
	    multiselect: true,
	    pager: "#js_gridPager",
	    jsonReader: {
	        root: "page.list",
	        page: "page.currPage",
	        total: "page.totalPage",
	        records: "page.totalCount"
	    },
	    prmNames: {
	        page: "page",
	        rows: "limit",
	        order: "order"
	    }
	});
});

//声明vue
var vm = new Vue({
	delimiters: ['[[', ']]'],//vue引用值使用双中括号(避免与django冲突)
	el: '#rrapp',
	data: {
		queryData: {
			macLike: '',
			equNameLike: '',
			equType: ''
		},
		showType: 'grid',//grid列表; form表单; view详情
		entity: {},
		tempMac: '',
		onlinePs: []//在线的设备列表平
	},
	methods: {
		addPsVm: function() {
			vm.showType = 'form';
			$('#weekup_time').val('');
			$('#close_time').val('');
			vm.entity = {
				'equ_type': 'ps'//设备类型为画屏
			};
		},
		selOnlinePsVm: selOnlinePs,
		toBatchSetTimeVm: toBatchSetTime,
		saveVm: saveFunc,
		reloadVm: reloadGrid,
		searchGridVm: searchGridFunc
	}
});

//根据查询条, 执行数据查询
function searchGridFunc(){
	var $grid = $('#js_jqGrid');
	var postData = $grid.jqGrid("getGridParam", "postData");
	$.extend(postData, vm.queryData);
	$grid.jqGrid("setGridParam", {
	  	search: true
	}).trigger("reloadGrid", [{page: 1}]);
}
//列表刷新
function reloadGrid() {
	vm.showType = 'grid';
	$("#js_jqGrid").trigger("reloadGrid");
}

//从在线的画屏中选择
function selOnlinePs(){
	//请求所有的在线终端列表
	$.ajax({
		type: "get",
		url: '/base/terminal/my_online_ps',
		dataType : 'json',
		success: function(r) {
			if(r.code == 0) {
				vm.onlinePs = r.onlinePs;
			} else {
				vm.onlinePs = [];
			}
			layer.open({
				title: '选择在线终端',
				type: 1,//div形式的页面层
				content: $('#selOnlinePsDiv'),//这里content是一个dom
				shade: [0.1, '#fff'],//显示遮罩
				area: ['520px', '320px'],
				btn: ['确认选择', '取消'],//底部展示关闭按钮
				btn1: function(index) {
					if(vm.tempMac){
						Vue.set(vm.entity, 'mac', vm.tempMac);
						layer.close(index);//选择完毕后关闭弹窗
					} else {
						_alertError('请选择一个在线终端！');
					}
				},
				btn2: function(index) {
					layer.close(index);
				}
			});
		}
	});
}

//修改方法
function editFunc(id) {
	vm.showType = 'form';
	$.get("/base/terminal/by_id?id=" + id, function(r){
		var entity = r.entity;
		vm.entity = entity;
		$('#weekup_time').val(entity.weekup_time ? entity.weekup_time : '');
		$('#close_time').val(entity.close_time ? entity.close_time : '');
    });
}
//详情
function viewFunc(id){
	vm.showType = 'view';
	$.get("/base/terminal/by_id?id=" + id, function(r){
		vm.entity = r.entity;
    });
}

//删除(逻辑删除)
function delFunc(id) {
	_alertConfirm('是否确认删除？', function(){
		$.ajax({
			type: "post",
		    url: '/base/terminal/delete',
			data: {
				id: id
			},
		    dataType : 'json',
		    success: function(r){
				if(r.code == 0){
					_alertInfo('数据已删除！', reloadGrid);
				}else{
					_alertError(r.msg);
				}
			}
		});
	});
}

//保存方法
function saveFunc(event) {
	var $form = $('#js_form');
	if(! $form.valid()){
		return;
	}
	var entity = vm.entity;
	entity['weekup_time'] = $('#weekup_time').val();
	entity['close_time'] = $('#close_time').val();
	//当前点击对象(按钮)
	var saveBtnDom = event.currentTarget;
	saveBtnDom.disabled = true;//保存按钮不再可用, 防止重复提交
	$.ajax({
		type: 'POST',
		url: '/base/terminal/save',
		data: {
			entity: JSON.stringify(entity),
		},
		dataType: 'json',
		async: false,
		success: function(jsonData) {
			if ('0' == jsonData.code) {
				_alertInfo('操作成功！', function(){
					reloadGrid();
	          		saveBtnDom.disabled = false;
				});
			} else {
	          	_alertError(jsonData.msg, function(){
					saveBtnDom.disabled = false;
	          	});
			}
		}
	});
}

//设置开关机时间
function toBatchSetTime(){
	//判断是否选择了设置行
	var $grid = $('#js_jqGrid');
	var rowIds = $grid.jqGrid('getGridParam', 'selarrrow');
	if(! rowIds || ! rowIds.length) {
		_alertWarning('请选择批量的终端设备！');
		return;
	}
	$('#set_weekup_time').val('');
	$('#set_close_time').val('');
	layer.open({
		title: '设置开关机时间',
		type: 1,//div形式的页面层
		content: $('#setTimesDiv'),//这里content是一个dom
		shade: [0.1, '#fff'],//显示遮罩
		area: ['520px', '320px'],
		btn: ['确认设置', '取消'],//底部展示关闭按钮
        btn1: function(index) {
        	var weekup_time = $('#set_weekup_time').val();
        	var close_time = $('#set_close_time').val();
        	if(! weekup_time && ! close_time){
        		_alertWarning('请选择设置的开关机时间！');
        		return;
        	}
			$.ajax({
				type: "post",
				url: '/base/terminal/batch_set_times',
				data: {
					ids: rowIds.join(','),
					weekup_time: weekup_time,
					close_time: close_time
				},
				dataType : 'json',
				success: function(r){
					if(r.code == 0){
						_alertInfo('操作完成！', function(){
							layer.close(index);
							reloadGrid();
						});
					}else{
						_alertError(r.msg);
					}
				}
			});
        },
        btn2: function(index) {
            layer.close(index);
        }
	});
}
