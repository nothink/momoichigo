"""Tests for ResourceQueueViewSet."""

from __future__ import annotations

import random
import shutil
from typing import Any

import pytest
from rest_framework.test import APIRequestFactory

from momoichigo.app.models import Resource, ResourceQueue
from momoichigo.app.views import ResourceQueueViewSet

pytestmark = pytest.mark.django_db


class TestResourceQueueView:
    """Tests for '/resource_queues/' ."""

    endpoint = "/api/resource_queues/"

    def test_list_empty_queue_ok(
        self: TestResourceQueueView,
        factory: APIRequestFactory,
    ) -> None:
        """Test for list empty (GET)."""
        assert len(ResourceQueue.objects.all()) == 0

        request = factory.get(self.endpoint)
        response = ResourceQueueViewSet.as_view({"get": "list"})(request)

        assert response.status_code == 204
        assert len(ResourceQueue.objects.all()) == 0

    def test_list_single_queue_ok(
        self: TestResourceQueueView,
        factory: APIRequestFactory,
        resources: list[Any],
    ) -> None:
        """Test for list single (GET)."""
        item = resources[random.randrange(len(resources))]
        ResourceQueue.objects.create(resource=item)

        for resource in Resource.objects.all():
            assert bool(resource.file) is False

        # signals を止めているので、Queueはこれのみのはず
        assert len(ResourceQueue.objects.all()) == 1

        request = factory.get(self.endpoint)
        response = ResourceQueueViewSet.as_view({"get": "list"})(request)

        assert response.status_code == 202
        # Queueに残りが格納されていること
        assert len(ResourceQueue.objects.all()) == len(resources) - 1

        # clean up local checked files.
        shutil.rmtree(item.key.split("/")[0])

    def test_list_multi_queue_ok(
        self: TestResourceQueueView,
        factory: APIRequestFactory,
        resources: list[Any],
    ) -> None:
        """Test for list multi (GET)."""
        # 2 から len(resources)-1 件のいずれかでテスト
        multi_length = random.randint(2, len(resources) - 1)
        for item in resources:
            if len(ResourceQueue.objects.all()) >= multi_length:
                break
            ResourceQueue.objects.create(resource=item)

        for resource in Resource.objects.all():
            assert bool(resource.file) is False

        # signals を止めているので、Queueはこれらのみのはず
        assert len(ResourceQueue.objects.all()) == multi_length

        request = factory.get(self.endpoint)
        response = ResourceQueueViewSet.as_view({"get": "list"})(request)

        assert response.status_code == 202
        # Queueに残りが格納されていること
        assert len(ResourceQueue.objects.all()) == len(resources) - multi_length
        for queue in ResourceQueue.objects.all():
            assert bool(queue.resource.file) is False

        # clean up local checked files.
        shutil.rmtree(resources[0].key.split("/")[0])

    def test_second_list_queue_ok(
        self: TestResourceQueueView,
        factory: APIRequestFactory,
        resources: list[Any],
    ) -> None:
        """Test for list multi (GET)."""
        # 2 から len(resources)-1 件のいずれかでテスト
        multi_length = random.randint(2, len(resources) - 1)
        for item in resources:
            if len(ResourceQueue.objects.all()) >= multi_length:
                break
            ResourceQueue.objects.create(resource=item)

        for resource in Resource.objects.all():
            assert bool(resource.file) is False

        # signals を止めているので、Queueはこれらのみのはず
        assert len(ResourceQueue.objects.all()) == multi_length

        # 1回目
        request = factory.get(self.endpoint)
        response = ResourceQueueViewSet.as_view({"get": "list"})(request)

        assert response.status_code == 202
        # Queueに残りが格納されていること
        assert len(ResourceQueue.objects.all()) == len(resources) - multi_length
        for queue in ResourceQueue.objects.all():
            assert bool(queue.resource.file) is False

        # 1回目
        request = factory.get(self.endpoint)
        response = ResourceQueueViewSet.as_view({"get": "list"})(request)
        assert response.status_code == 202
        # Queueが空のこと
        assert len(ResourceQueue.objects.all()) == 0

        # clean up local checked files.
        shutil.rmtree(resources[0].key.split("/")[0])

    @pytest.mark.enable_signals
    def test_heavy_list_queue_ok(
        self: TestResourceQueueView,
        factory: APIRequestFactory,
    ) -> None:
        """Test for list heavy datas over 30sec. (GET)."""
        TARGET_TOP = (
            "https://dqx9mbrpz1jhx.cloudfront.net/vcard/ratio20/images/card/ssr_sample/"
        )

        # 150件のSSR mp4データ
        TARGETS = [
            f"{TARGET_TOP}01b10b69b1c62aa3f9895874be613eee.mp4",
            f"{TARGET_TOP}02ab15889ea2dbc8d5c92153e1c6f8c8.mp4",
            f"{TARGET_TOP}03db1bbb0f485295cc12f725e1ccd9d3.mp4",
            f"{TARGET_TOP}03db641c8489ae6b4f0612bab45f1783.mp4",
            f"{TARGET_TOP}03e885297f8f7a762e67b0e65647cce9.mp4",
            f"{TARGET_TOP}04ca906ac5410389ef1a5673d8cc1696.mp4",
            f"{TARGET_TOP}053d5298bd0e7941b12479c643f19a1e.mp4",
            f"{TARGET_TOP}07dded979823a3a5d288757cd5b0b6cb.mp4",
            f"{TARGET_TOP}0808e3f19f8f75b46d4900436c4c7527.mp4",
            f"{TARGET_TOP}08259b7522afcf3f8adfc76ca6a7fa24.mp4",
            f"{TARGET_TOP}08ead3abd31f37a8f94f75570140c18e.mp4",
            f"{TARGET_TOP}0a8abf20b6a4b155201d5ec7807ce825.mp4",
            f"{TARGET_TOP}0b7dcdfd1bf13514d09307a7a1a7a314.mp4",
            f"{TARGET_TOP}0cbfbb193556764808d3dd95ffcee730.mp4",
            f"{TARGET_TOP}0d259c73c8865cf3d1d7f1f6333fbeca.mp4",
            f"{TARGET_TOP}0d8a4fe0eed03510ddeab7a7c92c004a.mp4",
            f"{TARGET_TOP}0d8c292359953cbc064aa07c3192d7f4.mp4",
            f"{TARGET_TOP}0eec7355b80ff0053cc10b67dd929a78.mp4",
            f"{TARGET_TOP}107909d7f06d69e73c4c3460bbd60830.mp4",
            f"{TARGET_TOP}119f0068790542b0c361fa3b64aa318d.mp4",
            f"{TARGET_TOP}11cbbb4ff375a3ed1bc5f3f4a5259a6e.mp4",
            f"{TARGET_TOP}1347418ddf5b50a2c9049db0a16faff2.mp4",
            f"{TARGET_TOP}13e1eab3350cdc19158bd2caadc2d9d6.mp4",
            f"{TARGET_TOP}14ae4c595779d170370bfaa2fd6e01a7.mp4",
            f"{TARGET_TOP}14b811517a35556be43d2f7d5c9ff996.mp4",
            f"{TARGET_TOP}162a8c9d22493139b10ef0e2995c2e7b.mp4",
            f"{TARGET_TOP}16c57555a5753d7bd3cfc7ee5c805614.mp4",
            f"{TARGET_TOP}1705acb343f093b9ddb0530058515b11.mp4",
            f"{TARGET_TOP}1abc66e63eab06c1da9ada878ed9c1ab.mp4",
            f"{TARGET_TOP}1b4f818a1816dcdc1d27060021622fd7.mp4",
            f"{TARGET_TOP}1cba6b43970743f9cee68850c18e4e21.mp4",
            f"{TARGET_TOP}1e9ec8963ebdb669971a75c63b97a907.mp4",
            f"{TARGET_TOP}1ee315cda5c49eb9fcf2401d0af73a5e.mp4",
            f"{TARGET_TOP}1f9740693a74818bf81d3b5f4f249b8f.mp4",
            f"{TARGET_TOP}209bcdf804c598b4546f3ccbe4656c00.mp4",
            f"{TARGET_TOP}2125cecb4b53e32a40ad1327c8c27f57.mp4",
            f"{TARGET_TOP}218d5422156d3c0d13b0654553b29e5d.mp4",
            f"{TARGET_TOP}23d20fc58848c57674bb700afd3df17b.mp4",
            f"{TARGET_TOP}23ef3f4ed2c5eaa9693640578d04071b.mp4",
            f"{TARGET_TOP}2490cbf74fa31825f9596da7012df6ee.mp4",
            f"{TARGET_TOP}24a16b74620b25f94aa1fc4fc72665b7.mp4",
            f"{TARGET_TOP}251957cfdb120f467802e1a3888a951a.mp4",
            f"{TARGET_TOP}270f91c7a728dbcec3ddd50a1af4357c.mp4",
            f"{TARGET_TOP}2834890e746e780d3f86bc6a8cc3f6a9.mp4",
            f"{TARGET_TOP}2841bc15bd9a0837c348e24b25eb6d19.mp4",
            f"{TARGET_TOP}28be65d41c8fa962b60722fc79edbcf9.mp4",
            f"{TARGET_TOP}2942b04f335274e9d1bcdf5ccba10cce.mp4",
            f"{TARGET_TOP}29be01d9c9f3a0cda153793f51fd1249.mp4",
            f"{TARGET_TOP}2a312c68ecc5cc9b845da249797c938d.mp4",
            f"{TARGET_TOP}2a592fc8512bf26c260c7e44c3a50615.mp4",
            f"{TARGET_TOP}2a60c6e949878a3f4c4b009522e734e7.mp4",
            f"{TARGET_TOP}2a877d409ee2af262f60a42b65a07e64.mp4",
            f"{TARGET_TOP}2baf0d7b0bf00f90208737f36827763c.mp4",
            f"{TARGET_TOP}2c67ecf70b8bce17ffa0669668d2b575.mp4",
            f"{TARGET_TOP}2d67add94c9cb86b9b9f7b56495d9f01.mp4",
            f"{TARGET_TOP}300287b3829435bc3f045924bd8fc76c.mp4",
            f"{TARGET_TOP}3127679bc21d6cb094ad9834a2b9c8c1.mp4",
            f"{TARGET_TOP}3228b62f2960f2b6dbe2084d47f447f6.mp4",
            f"{TARGET_TOP}326564be8331820da757a60a1adcc133.mp4",
            f"{TARGET_TOP}328d1ad4bc19efc732b07f51c0e423af.mp4",
            f"{TARGET_TOP}32c422de1e6537ad5ba80ab0e67557cc.mp4",
            f"{TARGET_TOP}32c87fd1ca96524644bcc6274e7b0a46.mp4",
            f"{TARGET_TOP}33d09734c23e56a6c6776f4ab4c652f5.mp4",
            f"{TARGET_TOP}347213e79a7000d21596d738c1ced3c5.mp4",
            f"{TARGET_TOP}3637c21cf80529ea522cfd5115c159f4.mp4",
            f"{TARGET_TOP}37907b423f12df81ed24f55a4b975060.mp4",
            f"{TARGET_TOP}39855ae234c867e538dab535fefa8a70.mp4",
            f"{TARGET_TOP}3ad112ac42fd2b356bfc2c2d0b346696.mp4",
            f"{TARGET_TOP}3b33b151380401ecb02d54a708b20e3e.mp4",
            f"{TARGET_TOP}3e689d7710c5fead24609c2c3dc9c75f.mp4",
            f"{TARGET_TOP}400d5ea9fa97bad4af5a27e3d4bab668.mp4",
            f"{TARGET_TOP}411976b019e5cfa1fae0687661f2745a.mp4",
            f"{TARGET_TOP}41a48b09650dd791b44f65e8c3d1235e.mp4",
            f"{TARGET_TOP}41e11076eaf9e3018473401e216e6b11.mp4",
            f"{TARGET_TOP}41f164617ce275e026bb2528ab0c8148.mp4",
            f"{TARGET_TOP}42cf2b89e611793a9fbe29fb21fd0119.mp4",
            f"{TARGET_TOP}441104e4f49a915a91017050428b8c35.mp4",
            f"{TARGET_TOP}447b5cfdd06524f440ba799a8f7de5da.mp4",
            f"{TARGET_TOP}44e71488acd4646bb18cb6dd3db3c4a1.mp4",
            f"{TARGET_TOP}45c0b2a2e93c48f7b1e0567d0ff26e54.mp4",
            f"{TARGET_TOP}45ca7cf3e4ff2ab6f8e7548bf0d08f97.mp4",
            f"{TARGET_TOP}4672e9b8980c64266ac4da60e952f49a.mp4",
            f"{TARGET_TOP}467862df54e3630c90b11e6fc10b64bc.mp4",
            f"{TARGET_TOP}46e682d1d9167ef1335b49e8654b0c97.mp4",
            f"{TARGET_TOP}4714959937d0f3ee7c5f12f3dab7e565.mp4",
            f"{TARGET_TOP}489b494c5e3cce9d955cc1adfdc4ff78.mp4",
            f"{TARGET_TOP}48b43fc497ca77a7aceea1fff04cec8c.mp4",
            f"{TARGET_TOP}49972e7544917910925003316e7ad8ac.mp4",
            f"{TARGET_TOP}49e4f33e3f637c6891e1523679d9f151.mp4",
            f"{TARGET_TOP}4b901ea320adb8522f728252b74ad9b1.mp4",
            f"{TARGET_TOP}4bde801eca96c1dcd92ea595ff32fa29.mp4",
            f"{TARGET_TOP}4ca6e00fdafcc4db56cc5292e5426f56.mp4",
            f"{TARGET_TOP}4d14241244fc87976792d7718d66c06c.mp4",
            f"{TARGET_TOP}4d900ff9e7d4903bd92976ee55ad5c10.mp4",
            f"{TARGET_TOP}4def240876ade0979827de23be7f1c84.mp4",
            f"{TARGET_TOP}4e6bbb59f400c2c8a0df898951d0c2bd.mp4",
            f"{TARGET_TOP}4e9ceb901073f3d61b6b00f230f62313.mp4",
            f"{TARGET_TOP}4ef49a9270ff59ae0cd5ea674a992ac4.mp4",
            f"{TARGET_TOP}5151072efb5a15c7ef6e9f6e3dfc8c91.mp4",
            f"{TARGET_TOP}522603ef52324db4e079ae28c939e03d.mp4",
            f"{TARGET_TOP}52565a383464b5e84777c179b74c2af1.mp4",
            f"{TARGET_TOP}5299b68452c26d7cb1e55e5f50be974c.mp4",
            f"{TARGET_TOP}53576f5355392b366e05d916d0673a65.mp4",
            f"{TARGET_TOP}5375e6eda7cfdef3a79cc4611abbe8ca.mp4",
            f"{TARGET_TOP}569572705a8389dc995843c33cb6b12d.mp4",
            f"{TARGET_TOP}5978c3fd3eeebbc6205676f753c87a6c.mp4",
            f"{TARGET_TOP}5984220643b665673adff92998b0b76b.mp4",
            f"{TARGET_TOP}5a79739d54027f9feee380b24485b940.mp4",
            f"{TARGET_TOP}5b0a381f070913c29e8db3fc77d89d95.mp4",
            f"{TARGET_TOP}5bef6928624f9a50b2fb1b7cb174cf6c.mp4",
            f"{TARGET_TOP}5c6a6ba87df95a7ce2e26d59cc994b01.mp4",
            f"{TARGET_TOP}5ccde19a74b4d08438fd926f7c15bd73.mp4",
            f"{TARGET_TOP}5d14c946ce22a7d8ca24d70a04cc9cbe.mp4",
            f"{TARGET_TOP}5d4c4924306386bcf1fe1118bbdc5a89.mp4",
            f"{TARGET_TOP}5dd955716fd99fb1109099e351d31087.mp4",
            f"{TARGET_TOP}5ee9ea9e02316df5e8eb0b28ee622e5e.mp4",
            f"{TARGET_TOP}5f945e9a4e49e2a5381a568df5a08699.mp4",
            f"{TARGET_TOP}619ae084c4a54b8608c496d402020c0c.mp4",
            f"{TARGET_TOP}6267c6aaaa92d438a3340a9891ab6498.mp4",
            f"{TARGET_TOP}638bcbc799b8158d37f7c95f5b480951.mp4",
            f"{TARGET_TOP}639b2ec478ac9d694031ddae25de5476.mp4",
            f"{TARGET_TOP}656b8b841c8e5cbd7457c553fd9dee78.mp4",
            f"{TARGET_TOP}66641d3b2ff45f3181c8a17d01d44280.mp4",
            f"{TARGET_TOP}66816a81a50406d682f08e7d4afd4489.mp4",
            f"{TARGET_TOP}669ea34722e77bc76d9d48a175b18201.mp4",
            f"{TARGET_TOP}68e99a70c7c98a6b3baa3c807e0d2519.mp4",
            f"{TARGET_TOP}69a8fe0b9f2e8dec307d2056800696a2.mp4",
            f"{TARGET_TOP}6d2ccbe49c3da9b2171989c67fe0919d.mp4",
            f"{TARGET_TOP}6d831dcae4ef902948294ece3d2057b1.mp4",
            f"{TARGET_TOP}6f163bcdecba2ab74cbf0921a1661fa2.mp4",
            f"{TARGET_TOP}6f28c0267cf09ba14a4206825bd8746f.mp4",
            f"{TARGET_TOP}7067e1d81eb983c54270022bfd3f00e1.mp4",
            f"{TARGET_TOP}70965061531337b315905baf09174344.mp4",
            f"{TARGET_TOP}72555421b854fa7a7a081e7aabbd2df4.mp4",
            f"{TARGET_TOP}74cda9b7082d88d78bd7a22a4e20f622.mp4",
            f"{TARGET_TOP}77ba0d6605c7a3f8842a6902047c5aac.mp4",
            f"{TARGET_TOP}7886a10aa1e7680c34c052f5c8601ddb.mp4",
            f"{TARGET_TOP}79996ef0cec794b64d178d96e1bc76e6.mp4",
            f"{TARGET_TOP}79b07c939e3d46de5cf7d32cf5331aa4.mp4",
            f"{TARGET_TOP}79fe2af54ed8b0172d3fcc65fd0de0f0.mp4",
            f"{TARGET_TOP}7b017dc81fa9d8952a8ac6abc8bab6f9.mp4",
            f"{TARGET_TOP}7bfe41990377912c5a5a5a50670f3a4a.mp4",
            f"{TARGET_TOP}7e20320c9f300f6853704b565fbf3977.mp4",
            f"{TARGET_TOP}7e288cf497b2ebb8205fff9f5d0efbe1.mp4",
            f"{TARGET_TOP}80386d921f31a057c6b0873a6a65f436.mp4",
            f"{TARGET_TOP}80b7cd872b06ba3828d235af228216d1.mp4",
            f"{TARGET_TOP}82a3e50edbb08d227908dc03776e6c2f.mp4",
            f"{TARGET_TOP}8311e2a4452106c02597574ee9d0e9ad.mp4",
            f"{TARGET_TOP}8332331829c271b23e8175e95d3939ca.mp4",
            f"{TARGET_TOP}834105d74f9582705b894d7fe75786c4.mp4",
            f"{TARGET_TOP}83c7dec1c5effb824e07dc9b855ce691.mp4",
            f"{TARGET_TOP}840f92b251592309eb3954e6756435a9.mp4",
            f"{TARGET_TOP}87f19d1bcb39ae20831f02082446e009.mp4",
            f"{TARGET_TOP}88c29cc9518f33107d8a6be9d89b7c6d.mp4",
            f"{TARGET_TOP}88f26d8d4c2db9cff315ed732c8f6ea6.mp4",
            f"{TARGET_TOP}8a8aa98a135faac8704b6f9d413e7d8b.mp4",
            f"{TARGET_TOP}8b1e9e861012bfe4ab35c8c7e251ae56.mp4",
            f"{TARGET_TOP}8b30669761ccf08548f0abb5d464d17f.mp4",
            f"{TARGET_TOP}8b54e7862ed23eccf7544ace58588565.mp4",
            f"{TARGET_TOP}8b797ad973a121b0e4a49382087cfdbf.mp4",
            f"{TARGET_TOP}8ba4f3cb9e47bc1b4426530bc626619c.mp4",
            f"{TARGET_TOP}8c41931c567a0b4c01a4f10648661b4a.mp4",
            f"{TARGET_TOP}8cd4e181696521ce5c2bb0ebb0df6d33.mp4",
            f"{TARGET_TOP}8d9aa3e3c630def6c94ef583a5a72760.mp4",
            f"{TARGET_TOP}8e737494e752bc5e6e056c93cc1e873e.mp4",
            f"{TARGET_TOP}8f66ef3ad0ae5f0b4cc5aaf50b1aa9c9.mp4",
            f"{TARGET_TOP}90fede291834b04dd6911af47ab1e60c.mp4",
            f"{TARGET_TOP}91a12f7e16dddbfdd376bd4a032de564.mp4",
            f"{TARGET_TOP}91bb1e0a897bb5bb77bc2d16e2498228.mp4",
            f"{TARGET_TOP}91ee189005502fae2550d876fe7b48d0.mp4",
            f"{TARGET_TOP}9205f1a1d39e690c92de62c759ee8bd2.mp4",
            f"{TARGET_TOP}9212f0d7de0c0df2e8bd1a407676de11.mp4",
            f"{TARGET_TOP}92b6c309dcc51fc41b496c9350b01aa5.mp4",
            f"{TARGET_TOP}935d19fc82263bc5c367445dcbf57a3c.mp4",
            f"{TARGET_TOP}9591ed62fda586a5b52da41202e60eb6.mp4",
            f"{TARGET_TOP}95ba919dc99abdbfcffd579d682d3f52.mp4",
            f"{TARGET_TOP}95e68c16dfb71f6f661eed9524f92abc.mp4",
            f"{TARGET_TOP}96d3d634632b46a49ad66dc56fd54c60.mp4",
            f"{TARGET_TOP}96dbb2605bc577a3d56983572a5b7d5d.mp4",
            f"{TARGET_TOP}974d9bd460a5601e8eaa63cbf3936f74.mp4",
            f"{TARGET_TOP}98a3880ea3f75fea49e4f9f7d345b589.mp4",
            f"{TARGET_TOP}990ecffb5622cdc2bfd3df0471831311.mp4",
            f"{TARGET_TOP}99151766ffdde8e5408ffa54184b372a.mp4",
            f"{TARGET_TOP}9a83bb090149c8237fefee916c4e681d.mp4",
            f"{TARGET_TOP}9a976f34f28234d8c9f928d3d056e426.mp4",
            f"{TARGET_TOP}9afc1e4c1800c5fdfd7f1dbede3c3a9d.mp4",
            f"{TARGET_TOP}9ba8fb8212ba79a15dfc1da54086a630.mp4",
            f"{TARGET_TOP}9be0e335118de5ff02ed2acfbe2b9d62.mp4",
            f"{TARGET_TOP}9d18477ae59bdb1e568ca12fc331a396.mp4",
            f"{TARGET_TOP}9e059195fb0c70896904f3844604eedc.mp4",
            f"{TARGET_TOP}9e466080ad0891fd8a7d2fad9d11ffbf.mp4",
            f"{TARGET_TOP}9f8496da72308388528c40492921451f.mp4",
            f"{TARGET_TOP}a15fc3ffa66d3fe2bbf55238459b67d6.mp4",
            f"{TARGET_TOP}a19dfa5bb87dcfe36da48dace6869787.mp4",
            f"{TARGET_TOP}a1c3b1609dc61524ba44d12be48c325b.mp4",
            f"{TARGET_TOP}a32f2dc2abc99861d961a5e26da51b44.mp4",
            f"{TARGET_TOP}a717a24c05d388e760625d23f2219718.mp4",
            f"{TARGET_TOP}a78f8f853828c613a28518a2db08c8ad.mp4",
            f"{TARGET_TOP}a867e6a1b94cf2d34ed6b206a0a643e8.mp4",
            f"{TARGET_TOP}a9786ec03c091fc99efa0dce30777df0.mp4",
        ]
        for target in TARGETS:
            Resource.objects.create(source=target)

        assert len(ResourceQueue.objects.all()) == len(TARGETS)

        request = factory.get(self.endpoint)
        response = ResourceQueueViewSet.as_view({"get": "list"})(request)

        assert response.status_code == 202
        assert len(ResourceQueue.objects.all()) > 0
        assert len(ResourceQueue.objects.all()) < len(TARGETS)

        # clean up local checked files.
        shutil.rmtree(Resource.objects.all()[0].key.split("/")[0])
