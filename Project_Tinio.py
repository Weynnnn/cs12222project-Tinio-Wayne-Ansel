from dataclasses import dataclass
from string import whitespace
import aiohttp 
import flet as ft
from flet.auth.oauth_provider import OAuthProvider
from flet.auth.authorization import Authorization
import base64

class Auth(Authorization):
    def __init__(self, *args, **kwargs):
        super(Auth, self).__init__(*args, **kwargs)

    def _Auth__get_default_headers(self):
        usrnme = "vLUaxSmSRocOjgPvv-LsXg" 
        encd = base64.b64encode(f'{usrnme}:'.encode('utf8')).decode('utf8')
        return {"User-Agent": f"Flet/0.6.2", "Authorization": f"Basic {encd}"}

@dataclass
class App:
    p: ft.Page
    @classmethod

    async def m(cls, p: ft.Page):
        p.title = "CS12 22.2 Project W.Tinio"
        b = 'https://www.reddit.com'
        pr = OAuthProvider(
            client_id = "vLUaxSmSRocOjgPvv-LsXg",
            client_secret = "",
            auth_endpoint = f"{b}/api/v1/authorize.compact?duration=permanent",
            token_endpoint = f"{b}/api/v1/access_token",
            redirect_url = "http://localhost/api/oauth/redirect",
            user_scopes = ['identity', 'read'])
        

        p.scroll = ft.ScrollMode.AUTO
        base_auth_url_text = ft.TextField(label='Base AUTH URL',prefix_text="https://www.reddit.com", autofocus=True)
        base_api_url_text = ft.TextField(label='Base API URL', prefix_text="https://oauth.reddit.com", autofocus=True)
        

        async def btn_on_click(enter):
            if base_auth_url_text.value == "":
                await get_link(pr, Auth)
            else:
                await p.update_async()

        login_btn = ft.ElevatedButton('Login', on_click = btn_on_click)
        await p.add_async(base_api_url_text, base_auth_url_text, login_btn)
        await p.update_async()
        
        async def on_login():
            if p.auth and p.auth.token:
                access_token = p.auth.token.access_token
                headers = {'Authorization': f'Bearer {access_token}'}
                request = aiohttp.request(
                    method='get',
                    url=f'https://oauth.reddit.com/new.json',
                    headers=headers,
                )
                
                async with request as link:
                    data = await link.json()
                    posts = data['data']['children']
                    print(posts)
                    post_controls = []
                    await p.clean_async()
                    await p.update_async()
                    refresh_btn = ft.IconButton(
                        icon=ft.icons.REFRESH,
                        icon_color="#f6edce",
                        icon_size=30,
                        tooltip="Refresh",
                        on_click=refresh
                    )
                    await p.add_async(
                        ft.Stack([
                            ft.Container(
                                refresh_btn,
                                expand=True,
                                alignment=ft.alignment.center_right,
                            ),
                            ft.Container(
                                ft.PopupMenuButton(
                                    items=[
                                        ft.PopupMenuItem(text="Logout", on_click=logout),
                                    ],
                                ),
                                left=30,
                            )
                        ])
                    )

                    async def downvote(event):
                        elem = lst_downvote_ctrls.index(event.control)
                        if lst_upvote_ctrls[elem].icon_color == 'orange':
                            lst_score_ctrls[elem].value = str(int(lst_score_ctrls[elem].value) - 2)
                            lst_upvote_ctrls[elem].icon_color = '#f6edce'
                            lst_downvote_ctrls[elem].icon_color = 'blue'

                        elif lst_upvote_ctrls[elem].icon_color != 'orange' and lst_downvote_ctrls[elem].icon_color == 'blue':
                            lst_score_ctrls[elem].value = str(int(lst_score_ctrls[elem].value) + 1)
                            lst_downvote_ctrls[elem].icon_color = '#f6edce'

                        else:
                            lst_score_ctrls[elem].value = str(int(lst_score_ctrls[elem].value) - 1)
                            lst_downvote_ctrls[elem].icon_color = 'blue'

                        await lst_downvote_ctrls[elem].update_async()
                        await lst_score_ctrls[elem].update_async()
                        await p.update_async()

                    async def upvote(event):
                        elem = lst_upvote_ctrls.index(event.control)
                        if lst_upvote_ctrls[elem].icon_color == 'orange' and lst_downvote_ctrls[elem].icon_color != 'blue':
                            lst_score_ctrls[elem].value = str(int(lst_score_ctrls[elem].value) - 1)
                            lst_upvote_ctrls[elem].icon_color = '#f6edce'
                        elif lst_downvote_ctrls[elem].icon_color == 'blue':
                            lst_score_ctrls[elem].value = str(int(lst_score_ctrls[elem].value) + 2)
                            lst_upvote_ctrls[elem].icon_color = 'orange'
                            lst_downvote_ctrls[elem].icon_color = '#f6edce'
                        else:
                            lst_score_ctrls[elem].value = str(int(lst_score_ctrls[elem].value) + 1)
                            lst_upvote_ctrls[elem].icon_color = 'orange'

                        await lst_upvote_ctrls[elem].update_async()
                        await lst_score_ctrls[elem].update_async()
                        await p.update_async()

                    lv = ft.ListView(expand=2, spacing=10, padding=10, auto_scroll=True)
                    lst_score_ctrls = []
                    lst_downvote_ctrls = []
                    lst_upvote_ctrls = []
                    
                    for elem, post in enumerate(posts):
                        title = post['data']['title'] 
                        num_comments = post['data']['num_comments']
                        author = post['data']['author']
                        subreddit = post['data']['subreddit']
                        score = post['data']['score']
                        likes = post['data']['likes']
                        

                        downvote_btn = ft.IconButton(
                            icon=ft.icons.ARROW_DOWNWARD,
                            icon_size=20,
                            icon_color='#f6edce',
                            tooltip="Downvote",
                            on_click=downvote,
                            style=ft.ButtonStyle(color={"selected": ft.colors.BLUE, "": ft.colors.BLACK})
                        )


                        upvote_btn = ft.IconButton(
                            icon=ft.icons.ARROW_UPWARD,
                            icon_size=20,
                            icon_color='#f6edce',
                            tooltip="Upvote",
                            on_click=upvote,
                            style=ft.ButtonStyle(color={"selected": ft.colors.ORANGE, "": ft.colors.BLACK})
                        )

                        score_txt = ft.Text(str(score), color="#f6edce")

                        lst_score_ctrls.append(score_txt)
                        lst_upvote_ctrls.append(upvote_btn)
                        lst_downvote_ctrls.append(downvote_btn)

                        lv.controls.append(
                            ft.Stack(
                                [
                                    ft.Container(
                                        height=120,
                                        bgcolor=ft.colors.TORTILLA,
                                        expand=True,
                                        border_radius=20
                                    ),

                                    ft.Container(
                                        upvote_btn,
                                        left=60,
                                        top=15,
                                        alignment=ft.alignment.center,
                                        expand=True
                                    ),

                                    ft.Container(
                                        score_txt,
                                        left=70,
                                        top=60,
                                        alignment=ft.alignment.center,
                                        expand=True
                                    ),

                                    ft.Container(
                                        downvote_btn,
                                        alignment=ft.alignment.center,
                                        left=50,
                                        top=75,
                                        expand=True
                                    ),

                                    ft.Container(
                                        content=ft.Text(f"{title}", no_wrap=True, color='#f6edce'),
                                        alignment=ft.alignment.center,
                                        top=35,
                                        left=150,
                                        expand=True
                                    ),
                                    
                                    ft.Container(
                                        content=ft.Text(f"{num_comments} comments {author} /r{subreddit}", color='#f6edce'),
                                        alignment=ft.alignment.center,
                                        top=65,
                                        left=150,
                                        expand=True
                                    ),
                                ],
                            )
                        )

                    await p.add_async(lv)
                    await p.update_async()        
            else:
                print("Login failed. Access token not available.")
            
        async def logout(e):
            await p.clean_async()
            await p.update_async()
            await App.m(p) 
        
        async def refresh(e):
            await p.clean_async()
            await p.update_async()
            await on_login()
            
        async def get_link(provider, authorization):
            await p.login_async(provider, authorization=Auth)
            while not (p.auth and p.auth.token):
                await p.update_async()
            await on_login()  
            
ft.app(target=App.m, port=80, view=ft.WEB_BROWSER)
