$(function () {
	//确定表格高度
	var gridHeight = $(document).height() - 178;//减的越少列表越高
	//初始化表格
	$('#js_jqGrid').jqGrid({
		url: '/base/log/log_query',
	    datatype: "json",
	    colModel: [
	       	{ name: 'id', hidden: true },
	    	{ label: '模块', name: 'module', width: 100 },
	    	{ label: '日志内容', name: 'content', width: 100 },
	    	{ label: '创建时间', name: 'create_time', width: 200 },
	        { label: '操作', name: 'operate', sortable: false, width: 200, formatter: function(cellValue, options, rowObject) {
	        	var operateBtn =
					'<a class="btn btn-sm btn-success" href=\'javascript:viewFunc("' + rowObject.id + '");\' >详情</a>';
	            return operateBtn;
	        }}
	    ],
		viewrecords: true,
	    height: gridHeight,
	    rowNum: 10,
		rowList : [10, 20, 50, 100, 200],
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

//详情
function viewFunc(id){
	vm.showType = 'view';
	$.get("/base/log/by_id?id=" + id, function(r){
		vm.entity = r.entity;
    });
}
