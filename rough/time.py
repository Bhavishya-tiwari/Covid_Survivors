import json

# y =  {
#     "group": "Website_Admins",
#     }


# myuserjson = json.dumps(y)
# print(myuserjson)

# sqr=[]

# i=0
# while i < 6:
#   sqr.append(i*i)
#   i += 0.01
#   print(sqr)


# sqr={}


# i=0
# while i < 6:
#   sqr[i*100]=i*i*100
#   i += 1

# for u in sqr:
#     print(sqr[u])
  






# import requests
# response = requests.get("http://api.open-notify.org/iss-now.json")
# print(response.status_code)


# o1 ={"q":"sdv","d":"dv"}
# print(o1+o1)


def passv(x):
    x = str(x)
    l = False
    ngap =True
    if(len(x)<8 and len(x)>5):
        l = True
    if(" " in x):
        ngap=False
    
    
    if(l == True and ngap == True):
        o = {
            "status":"v",
            "p":x
        }
        return o
    else:
        o = {"status":"n"}
        return o



print(passv("sdomcomcolk "))


