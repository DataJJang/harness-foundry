<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>${projectName}</title>
</head>
<body>
    <main>
        <h1>${projectName}</h1>
        <p>eGovFrame 기반 JSP/Spring MVC 시작 화면입니다.</p>
        <ul>
            <li>Repository: __REPOSITORY_NAME__</li>
            <li>Framework: ${framework}</li>
            <li>Next: controller, service, 공통 include/layout, KRDS 반영 범위를 정리하세요.</li>
        </ul>
    </main>
</body>
</html>
