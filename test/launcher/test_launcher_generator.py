from unittest import TestCase
from crudgen.code_generation.launcher import launcher_generator
from test.utils.files import check_files_are_identical


class TestLauncherGenerator(TestCase):
    def test_run(self):
        launcher_generator.run(
            ["table_1", "table_2"],
            None,
            None,
            ""
        )
        check_files_are_identical("app.py", "test/launcher/expected_launcher.py")

    def test_fast_content_setup(self):
        """ Test fastapi init statements generation """
        expected = "Base.metadata.create_all(bind=engine)\n" + \
                   "app = FastAPI()\n"
        generated = launcher_generator.fast_setup_content()
        self.assertEqual(expected, generated)

    def test_include_routes(self):
        """ Test include router generation """
        expected = "app.include_router(table_1_router.router)\n" + \
                   "app.include_router(table_2_router.router)\n"
        generated = launcher_generator.include_routers(["table_1", "table_2"])
        self.assertEqual(expected, generated)

    def test_exec_app(self):
        """ Test build exec app statement """
        expected = '\n\nif __name__ == "__main__":\n' + '    uvicorn.run(app, host="192.168.1.10",port=8085)\n'
        generated = launcher_generator.exec_app("192.168.1.10", 8085)
        self.assertEqual(expected, generated)
