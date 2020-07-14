
//layui table, 单击行选中事件
$(document).on("click", ".layui-table-body table.layui-table tbody tr", function (e) {
	if ($(e.target).hasClass("layui-table-col-special") || $(e.target).parent().hasClass("layui-table-col-special")) {
		return false;
	}
	var index = $(this).attr('data-index'), tableBox = $(this).closest('.layui-table-box'),
		tableFixed = tableBox.find(".layui-table-fixed.layui-table-fixed-l"),
		tableBody = tableBox.find(".layui-table-body.layui-table-main"),
		tableDiv = tableFixed.length ? tableFixed : tableBody,
		checkCell = tableDiv.find("tr[data-index=" + index + "]").find("td div.laytable-cell-checkbox div.layui-form-checkbox i"),
		radioCell = tableDiv.find("tr[data-index=" + index + "]").find("td div.laytable-cell-radio div.layui-form-radio i");
	if (checkCell.length) {
		checkCell.click();
	}
	if (radioCell.length) {
		radioCell.click();
	}
});

$(document).on("click", "td div.laytable-cell-checkbox div.layui-form-checkbox,td div.laytable-cell-radio div.layui-form-radio", function (e) {
	e.stopPropagation();
});

