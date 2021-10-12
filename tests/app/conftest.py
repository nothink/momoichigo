"""Config for All pytest fixtures."""

import random
from typing import Any

import pytest
from django.db.models.signals import post_save
from model_bakery import baker
from rest_framework.test import APIClient, APIRequestFactory

pytestmark = pytest.mark.django_db

# source のベースURL
URL_BASE = "https://dqx9mbrpz1jhx.cloudfront.net/vcard/"

# Resourceのファクトリで使う source のURL
SOURCE_URLS = [
    URL_BASE + "audio/voice/scenario/atlas/0b5d62c4dbf109d549153fb543078fa7/sprite.mp3",
    URL_BASE + "mp3/4925/1010_0c08ce73-7036-406a-b2fd-7b46bcc1ed00.mp3",
    URL_BASE + "mp3/4998/MYPAGE_b5235781-5a3e-469e-b722-e288db1401df.mp3",
    URL_BASE + "mp3/4998/MYPAGE_6a7839f5-8820-48c4-a452-1119693683d5.mp3",
    URL_BASE + "mp3/4998/MYPAGE_92ebd462-57da-4727-9bc7-a3260ac09aeb.mp3",
    URL_BASE + "ratio20/images/card/2b387c21824d4aa6bd7519adf6e1530f.jpg",
    URL_BASE + "ratio20/images/card/368663d7936a73985a7b0fdc010d7bb9.jpg",
    URL_BASE + "ratio20/images/card/413535f9464f8ddda9a514c87ba82e6d.jpg",
    # URL_BASE + "ratio20/images/card/4f583f313fadcf5e02455e2a8d812c56.jpg",
    # URL_BASE + "ratio20/images/card/8057cc6ab01af36fea16ccc4952ee910.jpg",
    # URL_BASE + "ratio20/images/card/87e9498c06622875eaa2774f452c9d2c.jpg",
    # URL_BASE + "ratio20/images/card/a3d9cb8cff48b1bec8334b8d53eaec2f.jpg",
    # URL_BASE + "ratio20/images/card/gif/053d5298bd0e7941b12479c643f19a1e.gif",
    # URL_BASE + "ratio20/images/card/gif/0fdec0b58da46363e641eae6b1837c14.gif",
    # URL_BASE + "ratio20/images/card/gif/1340b8183a18d608ccfb6fd505b5c8c9.gif",
    # URL_BASE + "ratio20/images/card/gif/209bcdf804c598b4546f3ccbe4656c00.gif",
    # URL_BASE + "ratio20/images/card/gif/251957cfdb120f467802e1a3888a951a.gif",
    # URL_BASE + "ratio20/images/card/gif/2ae7eec12892f9eff6d17abcfc0e3fec.gif",
    URL_BASE + "ratio20/images/card/mypage/92469f02bbbaf3ed1c09f2ac03c2228f.jpg",
    URL_BASE + "ratio20/images/precious/l/987617ec184d2e1f50ab3d8f738ea395.jpg",
    URL_BASE + "ratio20/images/scenario/girl/800x960/2_NuWTUqsW/girl_1.png",
]

HEAVY_SOURCE_URLS = [
    URL_BASE + "ratio20/images/card/ssr_sample/01b10b69b1c62aa3f9895874be613eee.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/02ab15889ea2dbc8d5c92153e1c6f8c8.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/03db1bbb0f485295cc12f725e1ccd9d3.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/03db641c8489ae6b4f0612bab45f1783.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/03e885297f8f7a762e67b0e65647cce9.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/04ca906ac5410389ef1a5673d8cc1696.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/053d5298bd0e7941b12479c643f19a1e.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/07dded979823a3a5d288757cd5b0b6cb.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/0808e3f19f8f75b46d4900436c4c7527.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/08259b7522afcf3f8adfc76ca6a7fa24.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/08ead3abd31f37a8f94f75570140c18e.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/0a8abf20b6a4b155201d5ec7807ce825.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/0b7dcdfd1bf13514d09307a7a1a7a314.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/0cbfbb193556764808d3dd95ffcee730.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/0d259c73c8865cf3d1d7f1f6333fbeca.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/0d8a4fe0eed03510ddeab7a7c92c004a.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/0d8c292359953cbc064aa07c3192d7f4.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/0eec7355b80ff0053cc10b67dd929a78.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/107909d7f06d69e73c4c3460bbd60830.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/119f0068790542b0c361fa3b64aa318d.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/11cbbb4ff375a3ed1bc5f3f4a5259a6e.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/1347418ddf5b50a2c9049db0a16faff2.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/13e1eab3350cdc19158bd2caadc2d9d6.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/14ae4c595779d170370bfaa2fd6e01a7.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/14b811517a35556be43d2f7d5c9ff996.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/162a8c9d22493139b10ef0e2995c2e7b.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/16c57555a5753d7bd3cfc7ee5c805614.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/1705acb343f093b9ddb0530058515b11.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/1abc66e63eab06c1da9ada878ed9c1ab.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/1b4f818a1816dcdc1d27060021622fd7.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/1cba6b43970743f9cee68850c18e4e21.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/1e9ec8963ebdb669971a75c63b97a907.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/1ee315cda5c49eb9fcf2401d0af73a5e.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/1f9740693a74818bf81d3b5f4f249b8f.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/209bcdf804c598b4546f3ccbe4656c00.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/2125cecb4b53e32a40ad1327c8c27f57.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/218d5422156d3c0d13b0654553b29e5d.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/23d20fc58848c57674bb700afd3df17b.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/23ef3f4ed2c5eaa9693640578d04071b.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/2490cbf74fa31825f9596da7012df6ee.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/24a16b74620b25f94aa1fc4fc72665b7.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/251957cfdb120f467802e1a3888a951a.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/270f91c7a728dbcec3ddd50a1af4357c.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/2834890e746e780d3f86bc6a8cc3f6a9.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/2841bc15bd9a0837c348e24b25eb6d19.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/28be65d41c8fa962b60722fc79edbcf9.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/2942b04f335274e9d1bcdf5ccba10cce.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/29be01d9c9f3a0cda153793f51fd1249.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/2a312c68ecc5cc9b845da249797c938d.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/2a592fc8512bf26c260c7e44c3a50615.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/2a60c6e949878a3f4c4b009522e734e7.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/2a877d409ee2af262f60a42b65a07e64.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/2baf0d7b0bf00f90208737f36827763c.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/2c67ecf70b8bce17ffa0669668d2b575.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/2d67add94c9cb86b9b9f7b56495d9f01.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/300287b3829435bc3f045924bd8fc76c.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/3127679bc21d6cb094ad9834a2b9c8c1.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/3228b62f2960f2b6dbe2084d47f447f6.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/326564be8331820da757a60a1adcc133.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/328d1ad4bc19efc732b07f51c0e423af.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/32c422de1e6537ad5ba80ab0e67557cc.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/32c87fd1ca96524644bcc6274e7b0a46.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/33d09734c23e56a6c6776f4ab4c652f5.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/347213e79a7000d21596d738c1ced3c5.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/3637c21cf80529ea522cfd5115c159f4.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/37907b423f12df81ed24f55a4b975060.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/39855ae234c867e538dab535fefa8a70.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/3ad112ac42fd2b356bfc2c2d0b346696.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/3b33b151380401ecb02d54a708b20e3e.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/3e689d7710c5fead24609c2c3dc9c75f.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/400d5ea9fa97bad4af5a27e3d4bab668.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/411976b019e5cfa1fae0687661f2745a.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/41a48b09650dd791b44f65e8c3d1235e.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/41e11076eaf9e3018473401e216e6b11.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/41f164617ce275e026bb2528ab0c8148.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/42cf2b89e611793a9fbe29fb21fd0119.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/441104e4f49a915a91017050428b8c35.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/447b5cfdd06524f440ba799a8f7de5da.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/44e71488acd4646bb18cb6dd3db3c4a1.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/45c0b2a2e93c48f7b1e0567d0ff26e54.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/45ca7cf3e4ff2ab6f8e7548bf0d08f97.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/4672e9b8980c64266ac4da60e952f49a.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/467862df54e3630c90b11e6fc10b64bc.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/46e682d1d9167ef1335b49e8654b0c97.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/4714959937d0f3ee7c5f12f3dab7e565.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/489b494c5e3cce9d955cc1adfdc4ff78.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/48b43fc497ca77a7aceea1fff04cec8c.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/49972e7544917910925003316e7ad8ac.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/49e4f33e3f637c6891e1523679d9f151.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/4b901ea320adb8522f728252b74ad9b1.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/4bde801eca96c1dcd92ea595ff32fa29.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/4ca6e00fdafcc4db56cc5292e5426f56.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/4d14241244fc87976792d7718d66c06c.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/4d900ff9e7d4903bd92976ee55ad5c10.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/4def240876ade0979827de23be7f1c84.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/4e6bbb59f400c2c8a0df898951d0c2bd.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/4e9ceb901073f3d61b6b00f230f62313.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/4ef49a9270ff59ae0cd5ea674a992ac4.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/5151072efb5a15c7ef6e9f6e3dfc8c91.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/522603ef52324db4e079ae28c939e03d.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/52565a383464b5e84777c179b74c2af1.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/5299b68452c26d7cb1e55e5f50be974c.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/53576f5355392b366e05d916d0673a65.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/5375e6eda7cfdef3a79cc4611abbe8ca.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/569572705a8389dc995843c33cb6b12d.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/5978c3fd3eeebbc6205676f753c87a6c.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/5984220643b665673adff92998b0b76b.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/5a79739d54027f9feee380b24485b940.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/5b0a381f070913c29e8db3fc77d89d95.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/5bef6928624f9a50b2fb1b7cb174cf6c.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/5c6a6ba87df95a7ce2e26d59cc994b01.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/5ccde19a74b4d08438fd926f7c15bd73.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/5d14c946ce22a7d8ca24d70a04cc9cbe.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/5d4c4924306386bcf1fe1118bbdc5a89.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/5dd955716fd99fb1109099e351d31087.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/5ee9ea9e02316df5e8eb0b28ee622e5e.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/5f945e9a4e49e2a5381a568df5a08699.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/619ae084c4a54b8608c496d402020c0c.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/6267c6aaaa92d438a3340a9891ab6498.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/638bcbc799b8158d37f7c95f5b480951.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/639b2ec478ac9d694031ddae25de5476.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/656b8b841c8e5cbd7457c553fd9dee78.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/66641d3b2ff45f3181c8a17d01d44280.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/66816a81a50406d682f08e7d4afd4489.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/669ea34722e77bc76d9d48a175b18201.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/68e99a70c7c98a6b3baa3c807e0d2519.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/69a8fe0b9f2e8dec307d2056800696a2.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/6d2ccbe49c3da9b2171989c67fe0919d.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/6d831dcae4ef902948294ece3d2057b1.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/6f163bcdecba2ab74cbf0921a1661fa2.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/6f28c0267cf09ba14a4206825bd8746f.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/7067e1d81eb983c54270022bfd3f00e1.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/70965061531337b315905baf09174344.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/72555421b854fa7a7a081e7aabbd2df4.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/74cda9b7082d88d78bd7a22a4e20f622.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/77ba0d6605c7a3f8842a6902047c5aac.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/7886a10aa1e7680c34c052f5c8601ddb.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/79996ef0cec794b64d178d96e1bc76e6.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/79b07c939e3d46de5cf7d32cf5331aa4.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/79fe2af54ed8b0172d3fcc65fd0de0f0.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/7b017dc81fa9d8952a8ac6abc8bab6f9.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/7bfe41990377912c5a5a5a50670f3a4a.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/7e20320c9f300f6853704b565fbf3977.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/7e288cf497b2ebb8205fff9f5d0efbe1.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/80386d921f31a057c6b0873a6a65f436.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/80b7cd872b06ba3828d235af228216d1.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/82a3e50edbb08d227908dc03776e6c2f.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/8311e2a4452106c02597574ee9d0e9ad.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/8332331829c271b23e8175e95d3939ca.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/834105d74f9582705b894d7fe75786c4.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/83c7dec1c5effb824e07dc9b855ce691.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/840f92b251592309eb3954e6756435a9.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/87f19d1bcb39ae20831f02082446e009.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/88c29cc9518f33107d8a6be9d89b7c6d.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/88f26d8d4c2db9cff315ed732c8f6ea6.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/8a8aa98a135faac8704b6f9d413e7d8b.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/8b1e9e861012bfe4ab35c8c7e251ae56.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/8b30669761ccf08548f0abb5d464d17f.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/8b54e7862ed23eccf7544ace58588565.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/8b797ad973a121b0e4a49382087cfdbf.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/8ba4f3cb9e47bc1b4426530bc626619c.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/8c41931c567a0b4c01a4f10648661b4a.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/8cd4e181696521ce5c2bb0ebb0df6d33.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/8d9aa3e3c630def6c94ef583a5a72760.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/8e737494e752bc5e6e056c93cc1e873e.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/8f66ef3ad0ae5f0b4cc5aaf50b1aa9c9.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/90fede291834b04dd6911af47ab1e60c.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/91a12f7e16dddbfdd376bd4a032de564.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/91bb1e0a897bb5bb77bc2d16e2498228.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/91ee189005502fae2550d876fe7b48d0.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/9205f1a1d39e690c92de62c759ee8bd2.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/9212f0d7de0c0df2e8bd1a407676de11.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/92b6c309dcc51fc41b496c9350b01aa5.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/935d19fc82263bc5c367445dcbf57a3c.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/9591ed62fda586a5b52da41202e60eb6.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/95ba919dc99abdbfcffd579d682d3f52.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/95e68c16dfb71f6f661eed9524f92abc.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/96d3d634632b46a49ad66dc56fd54c60.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/96dbb2605bc577a3d56983572a5b7d5d.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/974d9bd460a5601e8eaa63cbf3936f74.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/98a3880ea3f75fea49e4f9f7d345b589.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/990ecffb5622cdc2bfd3df0471831311.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/99151766ffdde8e5408ffa54184b372a.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/9a83bb090149c8237fefee916c4e681d.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/9a976f34f28234d8c9f928d3d056e426.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/9afc1e4c1800c5fdfd7f1dbede3c3a9d.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/9ba8fb8212ba79a15dfc1da54086a630.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/9be0e335118de5ff02ed2acfbe2b9d62.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/9d18477ae59bdb1e568ca12fc331a396.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/9e059195fb0c70896904f3844604eedc.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/9e466080ad0891fd8a7d2fad9d11ffbf.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/9f8496da72308388528c40492921451f.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/a15fc3ffa66d3fe2bbf55238459b67d6.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/a19dfa5bb87dcfe36da48dace6869787.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/a1c3b1609dc61524ba44d12be48c325b.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/a32f2dc2abc99861d961a5e26da51b44.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/a717a24c05d388e760625d23f2219718.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/a78f8f853828c613a28518a2db08c8ad.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/a867e6a1b94cf2d34ed6b206a0a643e8.mp4",
    URL_BASE + "ratio20/images/card/ssr_sample/a9786ec03c091fc99efa0dce30777df0.mp4",
]

# -------------- Fixtures -------------- #


@pytest.fixture(autouse=True)  # Automatically use in tests.
def mute_signals(request: Any) -> None:
    """Muting signals.

    see also: https://www.cameronmaske.com/muting-django-signals-with-a-pytest-fixture/
    """
    # Skip applying, if marked with `enabled_signals`
    if "enable_signals" in request.keywords:
        return

    signals = [
        post_save,
    ]
    restore = {}
    for signal in signals:
        # Temporally remove the signal's receivers (a.k.a attached functions)
        restore[signal] = signal.receivers
        signal.receivers = []

    def restore_signals() -> None:
        """When the test tears down, restore the signals."""
        for signal, receivers in restore.items():
            signal.receivers = receivers

    # Called after a test has finished.
    request.addfinalizer(restore_signals)


# Client と RequestFactory の各ユースケースは以下を参照
# https://stackoverflow.com/a/31001001
# 簡易にまとめると
#   - RequestFactory はリクエストを作るだけなので、それをviewに突っ込んで確認する用
#   - Client はリクエスト-レスポンスを最後まで偽装するので、結果E2Eになる


@pytest.fixture
def factory() -> APIRequestFactory:
    """Fixture for Returning APIRequestFactory."""
    return APIRequestFactory()


@pytest.fixture
def client() -> APIClient:
    """Fixture for Returning APIClient."""
    return APIClient()


@pytest.fixture
def sources() -> list[str]:
    """Return source path strings."""
    return SOURCE_URLS


@pytest.fixture
def single_resource() -> Any:
    """Return baked Resource models."""
    src_str = SOURCE_URLS[random.randrange(len(SOURCE_URLS))]
    resource = baker.make("app.Resource", source=src_str)

    return resource


@pytest.fixture
def resources() -> list[Any]:
    """Return baked Resource models."""
    resources = []
    for url in SOURCE_URLS:
        model = baker.make("app.Resource", source=url)
        resources.append(model)
    return resources


@pytest.fixture
def resource_queues() -> list[Any]:
    """Return baked ResourceQueue models."""
    queues = []
    for url in SOURCE_URLS:
        model = baker.make("app.ResourceQueue", source=url)
        queues.append(model)
    return queues


@pytest.fixture
def heavy_queues() -> list[Any]:
    """Return baked ResourceQueue models for Heavy tests."""
    queues = []
    for url in HEAVY_SOURCE_URLS:
        model = baker.make("app.ResourceQueue", source=url)
        queues.append(model)
    return queues
