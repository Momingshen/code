// var fs = require("fs");
// var file = fs.readFileSync("./1/CryptoJS.js", {'encoding':"utf8"});
// eval(file)

var CryptoJS = require('crypto-js')
function getCrypData(t) {
    var e = CryptoJS.enc.Hex.parse(t)
      , n = CryptoJS.enc.Base64.stringify(e)
      , f = CryptoJS.enc.Utf8.parse("jo8j9wGw%6HbxfFn")
      , m = CryptoJS.enc.Utf8.parse("0123456789ABCDEF")
      , a = CryptoJS.AES.decrypt(n, f, {
        iv: m,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    })
      , r = a.toString(CryptoJS.enc.Utf8);
    return r.toString()
}

// var t = '95780ba0943730051dccb5fe3918f9fe1b6f2130681f99d5620c5497aa480f132591ed9b62d9d0b8896bc9ffb19df81e59abce87e31bcc6f2998f8fbc62eab2071c9d3e3cccf2e51a3295780b16a1296d30354b81c20843a513a91e2237d4376beedd9878b2e8391d882173f9a2c8e4c160a633bf56d86a365d97ab0e6d04441a374452d648eae53cb6def3fd7042b2980b60ab849d69caab27e2327950cb5583d44d9fa26a358f8bf39b5411fee4d659912d49deeb223fee3cad141006044dbaac9aeade8d499b74b791eb0e97783ff81cc13a615f31dda3b68d99f42cf5b6289978a2cbf71113c6651f6f9731647f413d2a883400e1b2e88bee5da146bc72381879e6dad3cce147d9fd8da4d0989a5b1b51bcdbb5357581c40c0a26ebea124d0abc645c84acbdf1b3c42f15b6a8c870ec64ad302ff4a129bc1004c5021e5fb48f34321a0bc62602d329f6f32fc930042700af17c69622325d571740ff8c259c04345d48b6070b28d9f2124f8055902c499452f1ad988c739099c95d9e5f63fe3bdf2d28cbb30937679df25d3fd5d5d4f6c1ce5f9d9b211c0384472dc25cf9dca5fbf8e53a7520d88f7e03ecff2b8b9fb8dc615c6d399d350bc5fa993dfb868adeff4b7634a342fee84c146af849c9d1ed377c17b415afafa12b5491284279bea34c0c481cd684491305d08af4793574dd72893c1f74c4ca25da1f61eaef4a332706341485f15d9b2ab5a50e567ee269311af8b9af61f176e1030b9f754a6f83b01fe20b23785e7a73b561085d3588067df867a0eb64be2d331ae28151861aafa68408fd72450af354902398d964be72e17ffb95da0c377be9e73883330f2d7966eee925e25a2dd9eda776a7e0fe8f3f3cc91f3d882baa178deac4a481eccb8413c5b150c4fe4c9a6bf0b8938b4860f288395c023b8145f28187b899f8400aa394da828e290472ce2af93a27cef130a136d06c00aaa71d9df21e45cfd7840479be570f8035def6c8a10c9f7543a6f1c68974b2443119d92b9dbe6166f8ba00729c2cfe0792d63a85c84a93bcd345f09c7508ff5fa1240f9ce14089521d797f9a06dec88593898527ddc1463ce442c904a1ae2fe11fb569c50540626508486ba8b9612bf70989edb097cfc9a60f420500ea2430e76d8c505a4c5574fb541f785fd7b916a866a0d158964d3bfe7d347394d3a7f8f755312b446e71299ac21c73f648c6738c3f1a8c0de87a0b402760a6e63ce6743d5ff0ccb5fa05be8fe003d2d7398d6212765d8cd219c247628cdc7e389b162ed19bd51333b173bb581881aebc3f1b05eb802ce823d5f1356a86fb62b12fa2d02f931a58c1c44cb964b7158989c9bf7715349cd17ffd7d691b85684b48b0632e49abf8081042f637e27c08ba9e9dcc9047243c87b49d20db94dae9d197e6c16b826c2137fa303c37c030d25235f738e4bec434de5883994af7df1ef1192ec9029885d3dda7aca2d981c355d722d9983f3856b3937caba8894f8e65d908441cf9f0b1c9f9d6a37f05c421a93f4b3db41752724c3534a75fee13c1044bf963318b78aa1563425411aa7f0d3d32181849ff53ae340224b8313e8f45a054944a070fabe16bee416543611d27468042cc251ff792bb6045d0f6704a0b0382776624b4f3f50246c865619e77f0ffddccaa22380dbe91077dab8082bf354c7f6fc61b619d25dbe59cf727dd170f3618b09485d892d7c3edf736a137ad76642b8e59f87f319e3cbf5207e2df9ef9696fd5f146dd5797abb07955501b518dbdb2be83388accef30fc072b34744632992d8238c89978204db0730d3c8a297b899a3200a0a24b2b856e994b609afbe719067a839888f5eacf7935630c5a29c3bf410ca7f806b54b0326f1a0362bb31a4798b387a6b60641dfe82804d23175a2ce18cf2e4e333c10b22a87bb1ba204ad5ed95b4c78fea707b73084bea71396bde194782ed2a4f8cd3661d1b06f5e8be70456a08e26f6eee48e1468089be670e7f899cce7ad133c1a290dee0421171afc66b76517e9d6912f0c4450523205df2bd6a5b65c255a5ca169835df2f3416284853e2672be913f29d4f9a320255924df699606344c23e3ef5e16cd8b53fac278e1861f398da6bbb281f33750f1041c6894b9ba535eb23db79c566ef1ecb295cdc6e502ac46e7a99c43d65459499c36c0d90afcd914c29d49e60fa5830c6032cab10b32dc226be258653d4df4f5edab230e91db4b12e7e0220ade03cfafc69debddbff8daa8dbc84974788a39f50f20ef0ab200fc17e025d22bc247d51376fec202d1cae4738c8cc5dbeb2781b5472601b3067763889270ced9d750231296fb326ac00b9c4cb96972b21d126c8ad890ba1e83fefc9aa78414591409cb9bdbfbaec3e60aeed3573b5d59449f61cd5db45e15df068e819a099ae1cf1f5dad27bd081a7889ab3a1090d93f9c160561516191fbbd053d9a62dfe1161a06db60f2bbd8945bd224dcd8de7f17425fe6660baece665b332cff3027abb3a263bca06401c4c0c0e80ae8a1fbb2afc298d87e3754f1370261ef6f84a0d68248d6c98accd4ee48723f016d0d38c9797fe93b6522822e10f0168ba5447138dd0fd07e85328268527f42fa8669657f0c07b567461628ef79d62416fb3cac385a157231aa755933c97afc429a8749991538197c25373329bf11628f527d06492cc23b460a56bec8dd2a2e801412df43c071bfc1c526568b994c4e96850216f2187711e53a7d6aa1c359490b8a7f6147c16943ca926475922c5ddf17c2c65c7aaef1741e08b960749394be7ec98823549873c0beb4146f225820bd240cac618d1fe9c3a339399b5f9f5c77cd9d3f1f8fe83a2f7f758ebf83513e1268d937390d796c77d01ffa8d40392532a3a4b886f782d6794186623b5cf4b2e163a976bb9751b6e2da80f5c9d1140cf3bead38527ef2839f665632856b2e518d4d4e384befde7ff66f773b4653b2e15fb32bc06bf7ba3154ecd112e25ad5c56373969e09dd947f9e757c218d4fe08ad5fa52331a6fd5d4bdd8b91c6aeffcfe27bc483a7f54d7935e58068ae0be0c0ac499b3e1dc2889cbeecc52e30c7c71b9c8bc2ef375ccb747a9a93e5b713e112bd1271f3e3608ab9a6269f37fffda6631f332fd41cc98fbdfe6573d2fd5ffcd12cc2b68d4cf775b6a594d523b78ea097c89904b8562a4541d196e073d33c7fab8b934bfd722106823b92887e643ae88c438eaa93bfdb95c7f9a6f657817838c2f55bed7c820d90b1de117d14b75b70fe4b619511b60cf89786f6fd41a0a379b336a26d2e6fb5a6bda97729dedaf490244c40640a1cd1b5c2e98a6c2a8febad1379b96ef97be13d5077c6b995b7ec270bcfb8c2afb4e3a5469c3a4ae80ad676af5fd049140ee605909a982aac21bbbe9096d7e94b074d50c92509e01b27a9f95e94f210804c72aa14c1ac787e0ddf9a104e81785808961eb796885bd91aa0b4017945a071e3f1c8c54f3fcd7820af9bb1c89ae98f928abbc80bb1b2f91112dbea7780801509274d136f09d5c2799b6423e08b2485f25ebb62b36d0a7eff58a7f6fe5a8c2143f93f100c142e474fc5d21676fac8472fa7dd91ef15bce2c0e9e9551abe5d6e5ea8646f07407452e71d9e459f99e6fadd85324fb367750047e1f97e2cca3995aaf701fd382e65a9e0989ad1cf8639bc02ff811fbe91987877442c0881d31d32698bf092d5acff9ae28b3fdbbca577f59fed4e321d430ebe139e3812f736182cef9a7d7dba00e5e5f08023360ed599634a2a6c2eaecd1ed372d4a485f6c1d204c99a2ff287a50733cda7e692a97b435b8b038ccf106dc86939b42a6eb35a9f73d29d2992839f44decbac460c53161b296ce2ca0795196062203a66980020f01db60e9175a538a063950b1ba15de62d8714ada0c81a8986a0020c756b37a742ed371bf02bf227120af2cb4c56c106cb317de1fea18da79a8dc944e1174ac413fe421923c81dac5258cd03cb8eaf803ed36c465ee8c940c2c2f329d6453d3848fa996de111b5acc547f609fed9a21ccf7db85434d6f661ac4729194aaac210649a04dc510db9044df28a398c50dc8d270f168bd94ac5523d38e3eb75f04a7699c5754f04164834c92a1e25271afdd83237967574758a07591d7ae3c3e3926f6247605b0b0382c8a62bb144388a21da1bf98244de21bd687cc453aa0388d600601bf71d2978c879ece1bc77427b19aaf9dfa6efeffe1810b89d6232c80ca3689f9a57a7ab89140958f9861a7b2fe36020d47e5580920697129176a6f97020870aa1e08a8d8832eaf9c67595e61dde4910e1af39c67df48a2edf0c5ca5e1bc8de147f1f9b368fb2ec71629e176ac0ea8e3abed3025821af0f770f30df2c1c5bee36c1550fac1cf8a130cf85c4fc9a9a20a17a559af343cfdaf4fb701364a7a9168c20555ce3242dcdf9f0611200afa40310bb52b127f3c640020fc2bed7febc99226585b26cbbb2289ca7beb57f504ae132c97349280351acf9a37e7079bdba14ad858c56bb03afc49bca364e59fac09b5d39bb7fa7e1ed4002dd49cbf56b8535b094c2dcd63e19b4af7ed067abdb8107b68001a1d9b47e4aebec5220c9eec84cd0b4e2fa4dc942f14682a2ceaea9b976e3a9ab5e0f24858697446697ae4230bbd2f7f1ec5f84cf54dee2685c287a22d3340c41628935064b565117ab8dbc1f304660f31ae8d6e3274a65a2e9e56e289db70bdde03117b203083ca43c6b4306a20b3b24115ed23704a33719b37c76bd79c5e933f6bde9375c200972abccb7899832dcbae22c98bc257bf3a5bc230ff4053a67274ecc99835370a95f512f55fa075d79ad7c687baa98e948fbe9fb7a130019238b5435813d3f0bc8134b65b8f9150aa7caeb0f4bd0be81694f4f6880ed3d745b489f53d529740612dd1cf36375047e152be09cf71f102632fbf39e92921ef6469bea5c8812adfbf07987ffc11a6f49ed8e2e9c0e56f55b62094836d8dc4ff42ced76dbab6b07a1b4a3537d660030e3613adf9730c059542859e04a2f9d3cfb55b78526ea0904a3dd1c933f2cfbacc67bff06c201880a8d7fdb56fae940a636c646007017e22b2fc999b882bca92824d3bde113b099163fcfd6d200bcda8b72b2edc477bf3a6a1f65cc4493ba731030ddd0cb527de8ccdfb8c1497391a3d6cc95f923b028061a5725dedff6bbd0b18e97f0578831fc3cc9ce067ca8f82de2fcbce3a4c2cf4bcc07658220cc4c1adf11d7db5e43b0a20d048a2b34327116425278f3c8c66bd2ac916d5caddecc4fefb0953e49f15f94cd1084f1cc383f2da58f143701cea9b8600d64067bf867a05f630db86d29bcfe1bc1447f5236ec53172ba9094ce02ba201f05a0d7ffe51f1ae84ccba433c3ebe294eb3aeda7d340cad48bcd71b057e683b2a6cd03190a6763e872dc9b51a0c367648002cdf8ba4abe648258ba0d36d21d783c2762bde3321bb7b4a1771edb8e84b33afdc3690fded3efef5b831e8c512fb1acb7940e997356ae9bd2ed055e0e1cacb21d8690299dd5350fe8110ef39ee5cb1b5d8cbbbc5d653ae3563cdb522f4357d61a91d191d61b01787ae183547b5308021ae0bacad9b1d982df69ec60d08655d98ffdea4f56aca496feb2646bd0b0af831af67ca366227d76bea33c9b55e19f2ec1a4934d7b40c62acccc5865ba98657cfc32f2525297d9bec05f1677d7550a5696ef529115ffe622b2ddf4c6013df9df902349b1aa788b32e025a453172d9a734db2c8a9f2e3a316d85d9b1b67d0a59e4f1e0ac540d9582e55bf749a10411217f25e876650981711559db178b42cb78ede6f9a1b00e5388b7dcc1b7bee4fbc7382cc46ba5d5e99353dfad3b60eec7646860709936166d6546a2849d56c75086ccf546f4ae5e92c749e264e24f7c3de65319c031ea25e6dd4d9d68fb7f2a4949aef6ccacfb1d2e1496d575a56e1317fd35520fb79cd23c9af6c4c07b533fdf66cd24126703e733ec4c704378b86df1f977156ff37c4884199c05a2a80ce8c0f759938ef3b296db915e8c07c39a44eb5ef3bb61d43e6f18fb5128751bd17fe6c30cc9f931b4d97e864e80791deb61f54313c11f1fefa45a4fb35b02d99d392954107dba1c165c57a8f0b05d30f1db48cb2dd6dc236a57f1d444631eee8db8929ee8545e3b2e5810c5c4d184d1765ba2216d7d97f7fe1c4fff4791d9fbf39ab6a3c6364f746d912048bd76eb0500199b14ca6ca3b274da1b0dcb847153a098c64efe816d98b2268b7664041f4c28350c573211e7c05d72428f681d43549568727edf142a63ffbfc0f4390f0dd90b7f1d32745360c58a726581da419f214107e5b331b7ffa54800d111242668d8b1d0c2964aa941f8c50cedea00a9f0c8353f918317bd9ac82f7000f57e59fc9e864f498e545a64f9feeb1e68d70ac6954e392357b3d10cc919b'
// console.log(getCrypData(t))