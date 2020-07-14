//序列化表单数据为对象的扩展方法
$.fn.serializeObj = function() {
	var o = {};
	var a = this.serializeArray();
	$.each(a, function() {
		if (o[this.name]) {
			if (! o[this.name].push) {
				o[this.name] = [o[this.name]];
			}
			o[this.name].push(this.value || '');
		} else {
			o[this.name] = this.value || '';
		}
	});
	return o;
};

//数组按照指定元素移除的方法(移除一个)
Array.prototype.removeObj = function(obj) {
	if(obj){
		for (var i=0, len=this.length; i<len ; i++) {
			if(this[i] == obj){
				this.splice(i, 1);
				return;
			}
		}
	}
};

//确认某个值是否存在于数组中
function _checkValExist(array, obj) {
	if(obj && array && array.length){
	    for (var j = 0, len = array.length; j < len; j++) {
	        if (obj == array[j]) {
	            return true;
	        }
	    }
	}
    return false;
}

//确认某个值是否存在于数组中 - 按照Id进行匹配
function _checkExistById(array, objId){
	if(objId && array && array.length){
		for (var j=0, len=array.length; j<len ; j++) {
			if(objId == array[j].id){
				return true;
			}
		}
	}
	return false;
}
//对象数组中, 获取指定元素的方法 - 按照Id进行匹配
function _getObjById(array, objId){
	if(objId && array && array.length){
		//遍历匹配数组中的值
		for (var j=0, len=array.length; j<len ; j++) {
			if(objId == array[j].id){
				return array[j];
			}
		}
	}
	return null;
}
//对象数组中, 移除指定元素的方法 - 按照Id进行匹配
function _removeObjById(array, objId) {
	if(objId && array && array.length){
	    //遍历删除数组中的值
	    for (var j = 0, len = array.length; j < len; j++) {
	        if (objId == array[j].id) {
	            array.splice(j, 1);
	            break;
	        }
	    }
	}
}
//对象数组中, 获取元素下标
function _getIndexById(array, objId) {
	if(objId && array && array.length) {
		for (var i = 0, len = array.length; i < len ; i++) {
			if (objId == array[i].id) {
				return i;
			}
		}
	}
	return '';
}

//利用当前时间, 生成伪UUID
function _genUUID() {
	return "u" + new Date().getTime() + '-' + Math.round(Math.random() * 1000);
}

//对象的克隆方法
function _cloneObj(obj){
	if(typeof(obj) != 'object' || obj == null){
		return obj;
	}
	var newObj = {};
	for(var key in obj) {
		newObj[key] = _cloneObj(obj[key]);
	}
	return newObj;
}


//验证手机号方法
function _validPhone(phone) {
	if(! phone){
		_alertError('请输入手机号！');
		return false;
	}
	if(phone.length != 11){
		_alertError('手机号位数错误！');
		return false;
	}
	var reg = /^[1][3,4,5,6,7,8,9][0-9]{9}$/;
	if (! reg.test(phone)) {
		_alertError('请输入正确的手机号！');
		return false;
	}
	return true;
}
//验证身份证号方法
function _validIdCard(idCard) {
	if(idCard){
		var reg = /^\d{6}(18|19|20|21)?\d{2}(0[1-9]|1[012])(0[1-9]|[12]\d|3[01])\d{3}(\d|X|x)$/;
		if (! reg.test(idCard)) {
			_alertError('请输入正确的身份证号！');
			return false;
		}
	}
	return true;
}

//layui展示年度选择下拉框
function _initLayYear(yearDomId){
	return {
		elem: '#' + yearDomId,
		type: 'year',
		showBottom: false,//去掉底部框取消/确定/清空按钮
		change: function(value, date, endDate){
			//change事件, 保证年度选择后即关闭, 无需再点击关闭按钮
			$('#' + yearDomId).val(value);
			if($('.layui-laydate').length) {
				$('.layui-laydate').remove();
			}
		}
	};
}
//layui展示年度-月度选择框
function _initLayMonth(monthDomId){
	return {
		elem: '#' + monthDomId,
		type: 'month',
		showBottom: false,//去掉底部框取消/确定/清空按钮
		change: function(value, date, endDate){
			//change事件, 保证年度选择后即关闭, 无需再点击关闭按钮
			$('#' + monthDomId).val(value);
			if($('.layui-laydate').length) {
				$('.layui-laydate').remove();
			}
		}
	};
}

/************************************ 提示消息与弹窗 ****************************************/
//弹出操作成功提示的方法(3s自动关闭)
function _alertInfo(msg, callBackFn){
	  layer.msg(msg, {
	      icon: 1,
	      btn: ['确定']
	  }, function(){
		  (callBackFn && typeof(callBackFn) === 'function') && callBackFn();
	  });
}
//弹出警告框(3s自动关闭)
function _alertWarning(msg, callBackFn){
	  layer.msg(msg, {
	      icon: 7,
	      btn: ['确定']
	  }, function(){
		  (callBackFn && typeof(callBackFn) === 'function') && callBackFn();
	  });
}
//弹出操作失败提示的方法(3s自动关闭)
function _alertError(msg, callBackFn) {
	layer.msg(msg, {
		icon: 5,
		btn: ['确定']
	}, function(){
		(callBackFn && typeof(callBackFn) === 'function') && callBackFn();
	});
}

//弹出操作成功提示的方法(不自动关闭)
function _alertLotInfo(msg, callBackFn){
	  layer.alert(msg, {
	      icon: 1,
	      btn: ['确定']
	  }, function(index){
		  (callBackFn && typeof(callBackFn) === 'function') && callBackFn();
		  layer.close(index);
	  });
}
//弹出警告框(不自动关闭)
function _alertLotWarning(msg, callBackFn){
	  layer.alert(msg, {
	      icon: 7,
	      btn: ['确定']
	  }, function(index){
		  (callBackFn && typeof(callBackFn) === 'function') && callBackFn();
		  layer.close(index);
	  });
}
//弹出操作失败提示的方法(不自动关闭)
function _alertLotError(msg, callBackFn) {
	layer.alert(msg, {
		icon: 5,
		btn: ['确定']
	}, function(index){
		(callBackFn && typeof(callBackFn) === 'function') && callBackFn();
		layer.close(index);
	});
}


//弹出提示框的方法
function _alertConfirm(msg, yesCallBackFn, noCallBackFn){
	layer.confirm(msg, {
		 btn: ['确定', '取消']//按钮
	}, function(index, layero){
		(yesCallBackFn && typeof(yesCallBackFn) === 'function') && yesCallBackFn();
		layer.close(index);
	}, function(){
		(noCallBackFn && typeof(noCallBackFn) === 'function') && noCallBackFn();
	});
}

//打开一个大弹窗
function _openFrameMax(title, url, endFunc){
	var width = '90%';
	var height = '90%';
	_openFrameSetSize(title, url, width, height, endFunc);
}
//打开一个比例中等弹窗
function _openFrameMedium(title, url, endFunc){
	var width = '75%';
	var height = '80%';
	_openFrameSetSize(title, url, width, height, endFunc);
}
//打开一个小弹窗的方法(600x400)
function _openFrameMin(title, url, endFunc){
	_openFrameSetSize(title, url, '720px', '580px', endFunc);
}

//title:弹窗标题; url:请求地址; width:宽度(字符串); height:高度(字符串)
function _openFrameSetSize(title, url, width, height, endFunc) {
	window.top.layer.open({
	    type: 2,
	    title: title,
	    shadeClose: false,
	    resize: false,//不允许拖动拉伸尺寸
	    shade : [0.01, '#fff'],//显示遮罩
	    area: [width, height],
	    content: url,
	    //弹窗销毁后执行的方法
	    end: function(){
	    	(endFunc && typeof(endFunc) === 'function') && endFunc();
	    }
	});
}

//关闭当前窗口(iframe页面关闭自身)
function _closeFrame(){
	var index = parent.layer.getFrameIndex(window.name);
	parent.layer.close(index);
}


//基于当前页面, 打开子弹窗(不调用top.layer.open, 保证parent作用域可用)
function _openChildFrameMax(title, url, endFunc){
	var width = '90%';
	var height = '90%';
	_openChildFrSetSize(title, url, width, height, endFunc);
}
//打开一个比例中等弹窗
function _openChildFrame(title, url, endFunc){
	var width = '75%';
	var height = '80%';
	_openChildFrSetSize(title, url, width, height, endFunc);
}

//title:弹窗标题; url:请求地址; width:宽度(字符串); height:高度(字符串)
function _openChildFrSetSize(title, url, width, height, endFunc) {
	layer.open({
	    type: 2,
	    title: title,
	    shadeClose: false,
	    resize: false,//不允许拖动拉伸尺寸
	    shade : [0.01, '#fff'],//显示遮罩
	    area: [width, height],
	    content: url,
	    //弹窗销毁后执行的方法
	    end: function(){
	    	(endFunc && typeof(endFunc) === 'function') && endFunc();
	    }
	});
}

/************************************** 树查询处理 ******************************************/
//通用 - 树查询按钮(基于ztree的前端查询)
function _queryTreeKey($ztreeObj, treeKey) {
	if(! treeKey){
		return null;
	}
	//模糊查询节点数据集合
	var nodes = $ztreeObj.getNodesByParamFuzzy("name", treeKey, null);
	if(nodes && nodes.length) {
		var node1st = nodes[0];
		$ztreeObj.expandNode(node1st, true, false, false);
		$ztreeObj.selectNode(node1st);//选中第一个查询结果
		//手动执行onClick(如果有)
		var onClickFn = $ztreeObj.setting.callback.onClick;
		if(onClickFn && typeof(onClickFn) === 'function'){
			onClickFn(null, null, node1st);
		}
		return nodes;
	} else {
		_alertWarning('未找到相关信息！');
		return null;
	}
}
//通用 - 点击选中下一个查询结果的方法
function _queryTreeNext($ztreeObj, nodes, index) {
	if(! nodes || ! nodes.length){
		return 0;
	}
	//确定新的结果下标, 并选中
	index = index+1 >= nodes.length ? 0 : index+1;
	var node = nodes[index];
	$ztreeObj.expandNode(node, true, false, false);
	$ztreeObj.selectNode(node);//选中第一个查询结果
	//手动执行onClick(如果有)
	var onClickFn = $ztreeObj.setting.callback.onClick;
	if(onClickFn && typeof(onClickFn) === 'function'){
		onClickFn(null, null, node);
	}
	return index;
}
