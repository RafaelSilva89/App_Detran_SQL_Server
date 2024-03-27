css = '''
<style>
.chat-message {
padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
background-color: #2f2b3e
}
.chat-message.bot {
background-color: #6d7b99
}
.chat-message .avatar {
width: 20%;
}
.chat-message .avatar.user img {
max-width: 80px; /* Ajuste o valor conforme necessário para o avatar do usuário */
max-height: 80px; /* Ajuste o valor conforme necessário para o avatar do usuário */
border-radius: 50%;
object-fit: cover;
}
.chat-message .avatar.bot img {
max-width: 70px; /* Ajuste o valor conforme necessário para o avatar do bot */
max-height: 70px; /* Ajuste o valor conforme necessário para o avatar do bot */
border-radius: 50%;
object-fit: cover;
}
.chat-message .message {
width: 80%;
padding: 0 1.5rem;
color: #fff;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
<div class="avatar bot">
<img src="https://i.ibb.co/GxFxZjj/image1.png">
</div>
<div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
<div class="avatar user">
<img src="https://i.im.ge/2024/02/22/g9vXQ1.Logo-Detran.png">
</div>
<div class="message">{{MSG}}</div>
</div>
'''
