r1=['not good']
r2=['list is good']
r1.sort()
r2.sort()
print(r1)
print(r2)
if r1.sort()==r2.sort():
    print("ok")
else:
    print("Not ok")