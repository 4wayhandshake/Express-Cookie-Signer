"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const path_1 = __importDefault(require("path"));
const cookie_parser_1 = __importDefault(require("cookie-parser"));
const cookie_session_1 = __importDefault(require("cookie-session"));
const auth_1 = __importDefault(require("./routers/auth"));
const app = (0, express_1.default)();
const port = 3000;
const args = process.argv.slice(2);
if (args.length < 2) {
    console.error(`Usage: ${process.argv.slice(0,2).join(' ')} <cookie_name> <signing_key>`);
    return;
}
// app.use((0, cookie_session_1.default)({
//     name: "download_session",
//     keys: ["8929874489719802418902487651347865819634518936754"],
//     httpOnly: false,
//     maxAge: 7 * 24 * 60 * 60 * 1000,
// }));
app.use((0, cookie_session_1.default)({
    name: args[0],
    keys: [args[1]],
    httpOnly: false,
    maxAge: 7 * 24 * 60 * 60 * 1000,
}));
app.use(express_1.default.urlencoded({ extended: false }));
app.use((0, cookie_parser_1.default)());
app.get("/", (req, res) => {
    res.sendFile(`${__dirname}/views/index.html`);
});
app.use("/auth", auth_1.default);
app.use("*", (req, res) => {
    res.sendFile(`${__dirname}/views/error.html`);
});
app.listen(port, "localhost", () => {
    console.log("Listening on ", port);
});
