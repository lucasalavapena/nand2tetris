
for i in range(16):
    print(f"Not (in=in[{i}], out=out[{i}]);")

for i in range(16):
    print(f"Or (a=a[{i}], b=b[{i}], out=out[{i}]);")

for i in range(16):
    print(f"And (a=a[{i}], b=b[{i}], out=out[{i}]);")

# Mux16.hdl
for i in range(16):
    print(f"Mux (a=a[{i}], b=b[{i}], sel=sel, out=out[{i}]);")


# Mux4Way16.hdl
for i in range(16):
    print(f"Mux(a=a[{i}], b=b[{i}], sel=sel[1], out=innermux{i});")
    print(f"Mux(a=c[{i}], b=d[{i}], sel=sel[1], out=outermux{i});")
    print(f"Mux (a=innermux{i}, b=outermux{i}, sel=sel[0]);")

    
    
