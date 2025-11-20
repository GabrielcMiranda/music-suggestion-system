import base64
from email.utils import quote
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.settings import Settings
from app.schemas import ShareProfileRequest, StandartOutput, UserMusic
from fastapi import HTTPException
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ShareService:
    
    # UseCase para compartilhar música por email
    @staticmethod
    async def share_music_by_email(dto: UserMusic, sender_username: str, recipient_email: str) -> StandartOutput:
        
        try:
            # carregar configs email .env
            smtp_server = Settings.SMTP_SERVER  
            smtp_port = Settings.SMTP_PORT      
            email_user = Settings.EMAIL_USER    
            email_password = Settings.EMAIL_PASSWORD
            
            # verificar se as configurações estão sendo carregadas
            print(f"SMTP Server: {smtp_server}")
            print(f"SMTP Port: {smtp_port}")
            print(f"Email User: {email_user}")
            print(f"Email Password: {'***' if email_password else 'NOT SET'}")
            
            if not all([smtp_server, smtp_port, email_user, email_password]):
                raise HTTPException(
                    status_code=500,
                    detail="Configurações de email não foram definidas corretamente"
                )
            
            # mensagem de email
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = recipient_email
            msg['Subject'] = f"🎵 {sender_username} compartilhou uma música com você!"
            
            # template do email 
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center; color: white;">
                        <h1>🎵 Nova Música Compartilhada!</h1>
                    </div>
                    
                    <div style="padding: 20px; background-color: #f9f9f9;">
                        <p>Olá!</p>
                        
                        <p><strong>{sender_username}</strong> compartilhou uma música incrível com você:</p>
                        
                        <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                            <h2 style="color: #333; margin-top: 0;">🎵 {dto.title}</h2>
                            <p style="color: #666; font-size: 16px;"><strong>Artista:</strong> {dto.artist}</p>
                            <p style="color: #666; font-size: 16px;"><strong>Gênero:</strong> {dto.genre}</p>
                            <p style="color: #666; font-size: 16px;"><strong>Álbum:</strong> {dto.album}</p>
                        </div>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <p style="color: #888; font-size: 12px;">
                                Este email foi enviado através do Sistema de Sugestão Musical
                            </p>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Função bloqueante que será executada em thread separada
            def send_email():
                print(f"Tentando conectar ao servidor SMTP: {smtp_server}:{smtp_port}")
                with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
                    print("Conexão estabelecida")
                    server.starttls()
                    print("TLS iniciado")
                    server.login(email_user, email_password)
                    print("Login realizado com sucesso")
                    server.send_message(msg)
                    print("Email enviado com sucesso")
            
            # Executar em thread separada para não bloquear
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, send_email)
            
            logging.info(f"Música '{dto.title}' compartilhada por email de {sender_username} para {recipient_email}")
            
            return StandartOutput(
                status_code=200,
                detail=f"Música '{dto.title}' compartilhada por email com sucesso!"
            )
        
        # exceções especificas para identificar o bendito erro  
        except smtplib.SMTPAuthenticationError as e:
            error_msg = f"Erro de autenticação SMTP: {str(e)}"
            print(error_msg)
            logging.error(error_msg)
            raise HTTPException(
                status_code=500, 
                detail="Erro de autenticação no email. Verifique as credenciais."
            )
        except smtplib.SMTPRecipientsRefused as e:
            error_msg = f"Destinatário recusado: {str(e)}"
            print(error_msg)
            logging.error(error_msg)
            raise HTTPException(
                status_code=400, 
                detail="Email de destinatário inválido."
            )
        except smtplib.SMTPException as e:
            error_msg = f"Erro SMTP ao enviar email: {str(e)}"
            print(error_msg)
            logging.error(error_msg)
            raise HTTPException(
                status_code=500, 
                detail=f"Erro SMTP: {str(e)}"
            )
        except Exception as e:
            error_msg = f"Erro inesperado ao compartilhar música: {str(e)}"
            print(error_msg)
            logging.error(error_msg)
            raise HTTPException(
                status_code=500, 
                detail=f"Erro interno: {str(e)}"
            )
    
    # UseCase para compartilhar perfil por email  
    @staticmethod
    async def share_profile_by_email(dto: ShareProfileRequest, sender_username: str, sender_favorite_genre: str, sender_profile_picture: str = None) -> StandartOutput:
        
        try:
            smtp_server = Settings.SMTP_SERVER  
            smtp_port = Settings.SMTP_PORT      
            email_user = Settings.EMAIL_USER    
            email_password = Settings.EMAIL_PASSWORD
            
            print(f"SMTP Server: {smtp_server}")
            print(f"SMTP Port: {smtp_port}")
            print(f"Email User: {email_user}")
            print(f"Email Password: {'***' if email_password else 'NOT SET'}")
            
            if not all([smtp_server, smtp_port, email_user, email_password]):
                raise HTTPException(
                    status_code=500,
                    detail="Configurações de email não foram definidas corretamente"
                )
            
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = dto.recipient_email
            msg['Subject'] = f"👤 {sender_username} quer conectar com você no Sistema Musical!"
            
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%); padding: 20px; text-align: center; color: white;">
                        <h1>👤 Novo Convite de Conexão!</h1>
                    </div>
                    
                    <div style="padding: 20px; background-color: #f9f9f9;">
                        <p>Olá!</p>
                        
                        <p><strong>{sender_username}</strong> gostaria de se conectar com você no Sistema de Sugestão Musical!</p>
                        
                        <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                            <div style="text-align: center; margin-bottom: 20px;">
                                {f'<img src="{sender_profile_picture}" alt="{sender_username}" style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 3px solid #ff6b6b; box-shadow: 0 4px 8px rgba(0,0,0,0.2);" />' if sender_profile_picture else f'<div style="width: 100px; height: 100px; background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%); border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; color: white; font-size: 32px; font-weight: bold;">{sender_username[0].upper()}</div>'}
                            </div>
                            
                            <h2 style="color: #333; text-align: center; margin: 15px 0;">@{sender_username}</h2>
                            
                            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
                                <p style="color: #666; font-size: 16px; margin: 5px 0;"><strong>🎵 Gênero Favorito:</strong> {sender_favorite_genre}</p>
                            </div>
                            
                            {f'<div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin: 15px 0;"><p style="color: #444; font-style: italic; margin: 0;">💬 "{dto.message}"</p></div>' if dto.message else ''}
                        </div>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{Settings.FRONTEND_URL or 'http://localhost:4200'}/login" 
                               style="background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%); 
                                      color: white; 
                                      padding: 12px 30px; 
                                      text-decoration: none; 
                                      border-radius: 25px; 
                                      font-weight: bold;
                                      display: inline-block;">
                                🎧 Conectar no Sistema Musical
                            </a>
                        </div>
                        
                        <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0;">
                            <p style="color: #856404; font-size: 14px; margin: 0; text-align: center;">
                                💡 <strong>Dica:</strong> Crie sua conta e descubra músicas incríveis baseadas nos seus gostos!
                            </p>
                        </div>
                        
                        <p style="color: #888; font-size: 12px; text-align: center; margin-top: 30px;">
                            Este convite foi enviado através do Sistema de Sugestão Musical
                        </p>
                    </div>
                </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            def send_email():
                print(f"Tentando conectar ao servidor SMTP: {smtp_server}:{smtp_port}")
                with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
                    print("Conexão estabelecida")
                    server.starttls()
                    print("TLS iniciado")
                    server.login(email_user, email_password)
                    print("Login realizado com sucesso")
                    server.send_message(msg)
                    print("Email de perfil enviado com sucesso")
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, send_email)
            
            logging.info(f"Perfil de '{sender_username}' compartilhado por email para {dto.recipient_email}")
            
            return StandartOutput(
                status_code=200,
                detail=f"Seu perfil foi compartilhado com {dto.recipient_email} com sucesso!"
            )
            
        except smtplib.SMTPAuthenticationError as e:
            error_msg = f"Erro de autenticação SMTP: {str(e)}"
            print(error_msg)
            logging.error(error_msg)
            raise HTTPException(
                status_code=500, 
                detail="Erro de autenticação no email. Verifique as credenciais."
            )
        except smtplib.SMTPRecipientsRefused as e:
            error_msg = f"Destinatário recusado: {str(e)}"
            print(error_msg)
            logging.error(error_msg)
            raise HTTPException(
                status_code=400, 
                detail="Email de destinatário inválido."
            )
        except smtplib.SMTPException as e:
            error_msg = f"Erro SMTP ao enviar email: {str(e)}"
            print(error_msg)
            logging.error(error_msg)
            raise HTTPException(
                status_code=500, 
                detail=f"Erro SMTP: {str(e)}"
            )
        except Exception as e:
            error_msg = f"Erro inesperado ao compartilhar perfil: {str(e)}"
            print(error_msg)
            logging.error(error_msg)
            raise HTTPException(
                status_code=500, 
                detail=f"Erro interno: {str(e)}"
            )