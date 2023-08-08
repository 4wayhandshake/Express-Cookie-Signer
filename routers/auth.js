"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const node_crypto_1 = __importDefault(require("node:crypto"));
const router = express_1.default.Router();

const hashPassword = (password) => {
    return node_crypto_1.default.createHash("md5").update(password).digest("hex");
};

function writeCookies(req,res,next) {
    try {
        const user = eval( '(' + req.body.user + ')' );
        req.session = user;
    } catch (error) {
        req.session = {result:"Error: Invalid input"};
        console.log(error);
    }
    next();
}

router.post("/api", writeCookies, (req, res) => {
    res.send("Contacted API.");
});

router.post("/", writeCookies, (req, res) => {
    res.redirect("/");
});


exports.default = router;
