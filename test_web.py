import web
from web import form

urls = (
    '/','index', 'forms'
)
render = web.template.render('templates')
vname = form.regexp(r".","must be valid")

register_form = form.Form(
    form.Textbox("username", description="Username"),
    form.Textbox("email", vname, description="NAME?!"),

    form.Button("submit", type="submit", description="Register"),

)
class index:

    # called when anyone makes a GET request for /
    def GET(self):
        # i = web.input()
        f = register_form()
        print(self.__str__())
        return render.index()

    def POST(self):
        i = web.input()

class register:
    def GET(self):
        f = register_form()
        return render.forms(f)

    def POST(self):
        f = register_form()
        print(f)
if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()
