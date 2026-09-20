# food1="薯片"
# food2="雪碧"
# num1=3
# num2=1
# price1=10.5
# price2=3.5
# total=num1*price1+num2*price2
# print("商品名称 商品数量 商品单价")
# print(food1,num1,price1,sep="       ")
# print(food2,num2,price2,sep="       ")  
# print("总价",total)   


# num1=input("请输入一个数字：")
# num2=input("请输入另一个数字：")
# result=int(num1)+int(num2)
# print(f"两个数字的和为：{result}")


# length=input("请输入矩形的长度：")
# width=input("请输入矩形的宽度：")
# area=int(length)*int(width)
# print("矩形的面积为：",area)


price=input("请输入消费的价格：")
if int(price)>=100:
    print(f"打九折后价格为：{int(price)*0.9}")
else:
    print(f"不打折，价格为：{int(price)}")