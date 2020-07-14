$(function () {
	//确定表格高度
	var gridHeight = $(document).height() - 178;//减的越少列表越高
	//初始化表格
	$('#js_jqGrid').jqGrid({
		url: '/sr/hardware/query_online',
	    datatype: "json",
	    colModel: [
	    	{ label: '名称', name: 'hostname', width: 200 },
	    	{ label: '设备IP', name: 'ip', width: 200 },
	    	{ label: 'mac地址', name: 'mac', width: 200 },
	    	{ label: '上线时间', name: 'online_time', width: 200 },
	        { label: '操作', name: 'operate', sortable: false, width: 200, formatter: function(cellValue, options, rowObject) {
	        	var operateBtn =
					'<a class="btn btn-sm btn-success" href=\'javascript:joinFunc("' + rowObject.id + '");\' >加入</a> ';
	            return operateBtn;
	        }}
	    ],
		viewrecords: true,
	    height: gridHeight,
	    rowNum: 100,
		rowList : [100],
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
		queryData: {},
		showType: 'grid',//grid列表; form表单; view详情
		entity: {}
	},
	methods: {
		reloadVm: reloadGrid,
		searchGridVm: searchGridFunc,
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

function join(id){
	_alertConfirm('是否绑定此设备到魔盒？', function(){
		$.ajax({
			type: "post",
		    url: '/sr/hardware/bind_hardware',
			data: {
				id: id
			},
		    dataType : 'json',
		    success: function(r){
				if(r.code == 0){
					_alertInfo('设备已绑定！', reloadGrid);
				}else{
					_alertError(r.msg);
				}
			}
		});
	});
}
