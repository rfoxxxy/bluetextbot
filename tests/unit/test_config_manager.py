class TestConfigManager:
    def test_supported_modules_is_list(self, config_manager):
        assert isinstance(config_manager.get_item("core", "supported_modules"),
                          list)

    def test_prod_is_bool(self, config_manager):
        assert isinstance(config_manager.get_item("telegram", "prod"), bool)

    def test_webapp_port_is_int(self, config_manager):
        assert isinstance(
            config_manager.get_item("features.webhook", "webapp_port"), int)

    def test_beta_token_is_str(self, config_manager):
        assert isinstance(config_manager.get_item("telegram", "beta_token"),
                          str)

    def test_throttling_is_float(self, config_manager):
        assert isinstance(config_manager.get_item("bot", "throttling"), float)
