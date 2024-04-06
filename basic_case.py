import logging

logger = logging.getLogger("TestCase")
logger.setLevel(logging.DEBUG)

class BaseCase:

    def __init__(self,):
        self.subcases = []
        self.failed_list = []
        self._init_subcases()


    def _init_subcases(self):
        for item_name in dir(self):
            if item_name.startswith("test"):
                item = getattr(self, item_name)
                if callable(item):
                    self.subcases.append(item_name)
        logger.info(f"Total subcase: {len(self.subcases)}")


    def setup(self):
        """
        用例执行前执行的操作
        """
        pass

    def teardown(self):
        """
        用例执行后执行的操作
        """
        pass

    def setup_subcase(self):
        """
        每个子用例运行前执行
        """
        pass

    def teardown_subcase(self):
        """
        每个子用例运行后执行的清理操作
        """
        pass

    def _run_with_exception_log(self, item):
        try:
            item()
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def run(self):
        # 执行setup
        if not self._run_with_exception_log(self.setup):
            return False
        
        # 执行用例
        for subcase_name in self.subcases:
            item = getattr(self, subcase_name)
            try:
                self.setup_subcase()
                item()
                self.teardown_subcase()
            except Exception as e:
                logger.exception(e)
                self.failed_list.append((subcase_name, e))

        # 执行teardown
        if not self._run_with_exception_log(self.teardown):
            return False
        
        return True

    def print_result(self):
        print(self.failed_list)