package __PACKAGE_NAME__.web;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {

    @GetMapping({"/", "/home.do"})
    public String home(Model model) {
        model.addAttribute("projectName", "__PROJECT_NAME__");
        model.addAttribute("framework", "eGovFrame 4.3 JSP/Spring MVC");
        return "home";
    }
}
