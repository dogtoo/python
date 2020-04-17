db.getCollection('TPEX').aggregate([
{
    $group:{
        '_id':{'group':'$group','groupCode':'$groupCode'},
        'codes': {$push:{'$code':'$name'}}
    }
},
{
    $project: {
        _id:0,
        group:'$_id.group',
        groupCode:'$_id.groupCode',
        code:'$codes'
    }
}
])