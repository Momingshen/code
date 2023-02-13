function random_1(e) {
    for (var n, i = [], r = function(e) {
        e = e;
        var n = 987654321
          , i = 4294967295;
        return function() {
            var r = ((n = 36969 * (65535 & n) + (n >> 16) & i) << 16) + (e = 18e3 * (65535 & e) + (e >> 16) & i) & i;
            return r /= 4294967296,
            (r += .5) * (Math.random() > .5 ? 1 : -1)
        }
    }, o = 0; o < e; o += 4) {
        var s = r(4294967296 * (n || Math.random()));
        n = 987654071 * s(),
        i.push(4294967296 * s() | 0)
    }
    return {"words":i,"sigBytes":e}
}
var i = random_1(8)