import unittest


class RequiredSettingsTestCase(unittest.TestCase):
    def test_agent_url_setting(self):
        from deployments.settings import AGENT_URL

        self.assertEqual(AGENT_URL, None)

    def test_use_queue_setting(self):
        from deployments.settings import USE_QUEUE

        self.assertEqual(USE_QUEUE, None)

    def test_bootloader_url(self):
        from deployments.settings import BOOTLOADER_URL

        self.assertEqual(BOOTLOADER_URL, None)

    def test_broker_url(self):
        from deployments.settings import CELERY_SETTINGS

        self.assertIsInstance(CELERY_SETTINGS, dict)
        self.assertEqual(CELERY_SETTINGS['BROKER_URL'], None)
