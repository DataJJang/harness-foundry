package __PACKAGE_NAME__.web;

import org.junit.jupiter.api.Test;
import org.springframework.ui.ExtendedModelMap;

import static org.junit.jupiter.api.Assertions.assertEquals;

class HomeControllerTests {

    @Test
    void homeReturnsViewName() {
        HomeController controller = new HomeController();
        ExtendedModelMap model = new ExtendedModelMap();

        String viewName = controller.home(model);

        assertEquals("home", viewName);
        assertEquals("__PROJECT_NAME__", model.get("projectName"));
    }
}
