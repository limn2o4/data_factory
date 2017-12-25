# data_factory

A data set generator

## how to use it

this python code support three operations: generate new data set from
existed one , shuffle the index of each data,append more data to the original dataset

you can modify the work dictionary to specify the detail of your need
the new image will be locate in new_img

if you want to get a larger data set from a small number of data , you can change the dict by:

```buildoutcfg
     work_list = {'op':"new",'num': 100000,'mass':3,'is_norm_size':False,'size':None}
     
```

the first key means the operation you want to process and the 'num' key indicate the number of the expected data set
the key 'mass' is determine add how much noise or whether rotate or clip the image
te bigger number means more procedure.
the last two key you can chose to resize the image.

## future feature:

- more ways of process the image
- more options of maintain the data set
- interface or args

## license 

I don't really care the copyright of this code because seldom people will find this code.......