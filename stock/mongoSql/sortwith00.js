db.getCollection('stockDay').find({'date':'20200323',$or:[
                    {groupCode:{'$ne':'00'}}
                    ,{groupCode:{'$eq':'00'}, Transaction:{$gt:100}}
                 ]}).sort({Transaction:-1}).count()