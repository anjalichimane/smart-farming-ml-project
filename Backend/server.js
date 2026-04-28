

const express = require("express");
const cors = require("cors");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");


require("./db");
const User = require("./models/User");

const app = express();

app.use(cors());
app.use(express.json());

const SECRET_KEY = "agroai_secret_key"; // You can change this


// ================= SIGNUP =================
app.post("/signup", async (req, res) => {
  try {
    const { name, email, password } = req.body;

    const existing = await User.findOne({ email });
    if (existing)
      return res.json({ message: "User already exists" });

    const hashed = await bcrypt.hash(password, 10);

    const user = new User({ name, email, password: hashed });
    await user.save();

    res.json({ message: "Signup successful" });

  } catch (err) {
    res.status(500).json({ message: "Server error" });
  }
});


app.post("/login", async (req,res)=>{
  try{
    const {email,password} = req.body;

    const user = await User.findOne({email});
    if(!user)
      return res.json({message:"User not found"});

    const match = await bcrypt.compare(password,user.password);
    if(!match)
      return res.json({message:"Wrong password"});

    const token = jwt.sign(
      { id: user._id, name: user.name },
      "SECRET_KEY",
      { expiresIn: "1d" }
    );

    res.json({
      message:"Login successful",
      token,
      name: user.name
    });

  } catch(err){
    res.status(500).json({message:"Server error"});
  }
});


// ================= SERVER =================
app.listen(5000, () => {
  console.log("Server running on port 5000");
});




