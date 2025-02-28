import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;

@WebServlet("/bracket")
public class BracketServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        out.println("<h2>Login</h2>");
        out.println("<form method='POST' action='bracket'>");
        out.println("Username: <input type='text' name='username'><br>");
        out.println("Password: <input type='password' name='password'><br>");
        out.println("<input type='submit' value='Login'>");
        out.println("</form>");
        out.println("</body></html>");
    }

    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String username = request.getParameter("username");
        String password = request.getParameter("password");

        // Simple authentication (for demonstration purposes)
        if ("user".equals(username) && "pass".equals(password)) {
            HttpSession session = request.getSession();
            session.setAttribute("username", username);
            showBracketOptions(response);
        } else {
            response.sendRedirect("bracket");
        }
    }

    private void showBracketOptions(HttpServletResponse response) throws IOException {
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        out.println("<h2>Select Bracket Size</h2>");
        out.println("<form method='POST' action='createBracket'>");
        out.println("Choose size: <select name='size'>");
        out.println("<option value='4'>4</option>");
        out.println("<option value='8'>8</option>");
        out.println("<option value='12'>12</option>");
        out.println("<option value='16'>16</option>");
        out.println("<option value='32'>32</option>");
        out.println("<option value='64'>64</option>");
        out.println("<option value='128'>128</option>");
        out.println("</select><br>");
        out.println("Input items by ranking: <input type='text' name='items'><br>");
        out.println("Randomize items: <input type='checkbox' name='random'><br>");
        out.println("Make bracket public: <input type='checkbox' name='public'><br>");
        out.println("<input type='submit' value='Create Bracket'>");
        out.println("</form>");
        out.println("</body></html>");
    }
}
