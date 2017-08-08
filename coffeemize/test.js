


function once(callback) {
    var cached = undefined;

    return function () {
        if (cached !== undefined) {
            return cached;
        }

        cached = callback.apply(callback, arguments);
        return cached;
    }
}


var myAdd = once(function(a, b){return a+b;});

myAdd(5,6);
myAdd(3,4);