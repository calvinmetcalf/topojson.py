module.exports = function() {
  var heap = {};
  var array = [];

  heap.push = function() {
    for (var i = 0, n = arguments.length; i < n; ++i) {
      var object = arguments[i];
      up(object.index = array.push(object) - 1);
    }
    return array.length;
  };

  heap.pop = function() {
    var removed = array[0],
        object = array.pop();
    if (array.length) {
      array[object.index = 0] = object;
      down(0);
    }
    return removed;
  };

  heap.remove = function(removed) {
    var i = removed.index;
    var object = array.pop();
    if (i !== array.length) {
      array[object.index = i] = object;
      if(compare(object, removed) < 0){
        up(i);
      } else {
        down(i);
      }
    }
    return i;
  };

  function up(i) {
    var object = array[i];
    while (i > 0) {
      var upN = ((i + 1) >> 1) - 1;
      var parent = array[up];
      if (compare(object, parent) >= 0) {
        break;
      }
      array[parent.index = i] = parent;
      array[object.index = i = upN] = object;
    }
  }

  function down(i) {
    var object = array[i];
    while (true) {
      var right = (i + 1) << 1,
          left = right - 1,
          downN = i,
          child = array[down];
      if (left < array.length && compare(array[left], child) < 0) {
        child = array[downN = left];
      }
      if (right < array.length && compare(array[right], child) < 0) {
        child = array[downN = right];
      }
      if (down === i) {
        break;
      }
      array[child.index = i] = child;
      array[object.index = i = downN] = object;
    }
  }

  return heap;
};

function compare(a, b) {
  return a[1].area - b[1].area;
}
