"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const router = express_1.default.Router();

function writeCookies(req,res,next) {
    try {
        let user;
        if (req.body && req.body.user) {
            user = eval( '(' + req.body.user + ')' );
        } else if (req.query && req.query.user){
            user = eval( '(' + req.query.user + ')' );
        }
        req.session = user;
    } catch (error) {
        req.session = {result:"Error: Invalid input"};
        console.log(error);
    }
    next();
}

router.get("/api", writeCookies, (req, res) => {
    res.send("Contacted API.");
});

router.post("/", writeCookies, (req, res) => {
    res.redirect("/");
});


exports.default = router;
