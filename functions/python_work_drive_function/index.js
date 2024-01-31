const express = require('express');
const catalyst = require('zcatalyst-sdk-node')
const app = express()
app.use(express.json())
app.get('/checkallusers',async(req,res)=>{
	const capp = catalyst.initialize(req);
	const allusers = await capp.userManagement().getAllUsers();
	// console.log(allusers);
	res.status(200).send(allusers);
})
module.exports = app;
