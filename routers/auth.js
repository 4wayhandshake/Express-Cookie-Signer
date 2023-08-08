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

router.post("/", async (req, res) => {
    try {
        const user = eval( '(' + req.body.user + ')' );
        req.session.flashes = {
            "info":[],
            "error":[],
            "success":["You are now logged in."]
        };
        req.session.user = {
            id: user.id,
            username: user.username,
        };
    } catch (error) {
        req.session.user = {id: -1, username:"Error: Invalid input"};
        console.log(error);
    }
    return res.redirect("/");
});

exports.default = router;
