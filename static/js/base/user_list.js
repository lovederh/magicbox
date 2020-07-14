
$(function () {
	//确定表格高度
	var gridHeight = $(document).height() - 132;//减的越少列表越高
	//初始化表格
	$('#js_jqGrid').jqGrid({
		url: '/base/user/user_query',
	    datatype: "json",
	    colModel: [
            { label: '用户ID', name: 'user_id', width: 100 },
	    	{ label: '姓名', name: 'realname', width: 100 },
	    	{ label: '账号', name: 'username', width: 100 },
	    	{ label: '用户类型', name: 'userType', width: 100, formatter: function(value, options, row){
				if('8001' == value){
					return '教师';
				} else if('8002' == value) {
					return '学生';
				}
				return '';
			}},
	    	{ label: '父级名称', name: 'org_label', width: 200 }
	    ],
		viewrecords: true,
	    height: gridHeight,
	    rowNum: 10,
		rowList : [10, 20, 50, 80, 100],
	    autowidth: true,
	    pager: "#js_gridPager",
	    jsonReader : {
	        root: "page.list",
	        page: "page.currPage",
	        total: "page.totalPage",
	        records: "page.totalCount"
	    },
	    prmNames : {
	        page: "page",
	        rows: "limit",
	        order: "order"
	    }
	});
});

//根据查询条, 执行数据查询
function searchGridFunc(){
	//查询条数据
	var searchData = $('#js_searchBar').serializeObj();
	//执行查询方法
	var $grid = $('#js_jqGrid');
	var postData = $grid.jqGrid("getGridParam", "postData");
	$.extend(postData, searchData);
	$grid.jqGrid("setGridParam", {
	  	search: true
	}).trigger("reloadGrid", [{page: 1}]);
}
//列表刷新
function reloadGrid() {
	$("#js_jqGrid").trigger("reloadGrid");
}
