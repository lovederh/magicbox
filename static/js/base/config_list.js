$(function () {
	//确定表格高度
	var gridHeight = $(document).height() - 178;//减的越少列表越高
	//初始化表格
	$('#js_jqGrid').jqGrid({
		url: '/base/config/config_query',
	    datatype: "json",
	    colModel: [
	       	{ name: 'id', hidden: true },
	    	{ label: '参数值', name: 'key', width: 100 },
	    	{ label: '参数名', name: 'value', width: 100 },
	    	{ label: '备注', name: 'remark', width: 200 },
	        { label: '操作', name: 'operate', sortable: false, width: 200, formatter: function(cellValue, options, rowObject) {
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
			keyLike: '',
			valueLike: ''
		},
		showType: 'grid',//grid列表; form表单; view详情
		entity: {}
	},
	methods: {
		addVm: function() {
			vm.showType = 'form';
			vm.entity = {};
		},
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

//修改方法
function editFunc(id) {
	vm.showType = 'form';
	$.get("/base/config/by_id?id=" + id, function(r){
		vm.entity = r.entity;
    });
}
//详情
function viewFunc(id){
	vm.showType = 'view';
	$.get("/base/config/by_id?id=" + id, function(r){
		vm.entity = r.entity;
    });
}

//删除(逻辑删除)
function delFunc(id) {
	_alertConfirm('是否确认删除？', function(){
		$.ajax({
			type: "post",
		    url: '/base/config/delete',
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
	//当前点击对象(按钮)
	var saveBtnDom = event.currentTarget;
	saveBtnDom.disabled = true;//保存按钮不再可用, 防止重复提交
	$.ajax({
		type: 'POST',
		url: '/base/config/save',
		data: {
			entity: JSON.stringify(vm.entity),
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
