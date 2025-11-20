import resend
from app.core.settings import Settings
from app.schemas import UserMusic, ShareProfileRequest, StandartOutput
from fastapi import HTTPException
import logging

resend.api_key = Settings.RESEND_API_KEY

class EmailService:
    
    @staticmethod
    async def send_music_share(dto: UserMusic, sender_username: str, recipient_email: str) -> StandartOutput:
        """Compartilhar música por email usando Resend"""
        
        try:
            if not Settings.RESEND_API_KEY:
                raise HTTPException(
                    status_code=500,
                    detail="Resend API Key não configurada"
                )
        
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center; color: white;">
                        <h1>🎵 Nova Música Compartilhada!</h1>
                    </div>
                    
                    <div style="padding: 20px; background-color: #f9f9f9;">
                        <p style="font-size: 16px; color: #333;">
                            Olá! <strong>{sender_username}</strong> compartilhou uma música incrível com você:
                        </p>
                        
                        <div style="background-color: white; border-left: 4px solid #667eea; padding: 20px; margin: 20px 0; border-radius: 8px;">
                            <h2 style="margin: 0 0 10px 0; color: #667eea;">🎵 {dto.title}</h2>
                            <p style="margin: 5px 0; color: #666;"><strong>Artista:</strong> {dto.artist}</p>
                            <p style="margin: 5px 0; color: #666;"><strong>Álbum:</strong> {dto.album}</p>
                            <p style="margin: 5px 0; color: #666;"><strong>Gênero:</strong> {dto.genre}</p>
                        </div>
                        
                        <div style="background-color: #f0f4ff; padding: 15px; border-radius: 8px; margin: 20px 0;">
                            <p style="margin: 0; color: #555;">
                                💡 <strong>Dica:</strong> Descubra mais músicas incríveis no Rhythmate!
                            </p>
                        </div>
                        
                        <p style="color: #888; font-size: 12px; text-align: center; margin-top: 30px;">
                            Este email foi enviado através do Rhythmate
                        </p>
                    </div>
                </body>
            </html>
            """
            
            params = {
                "from": Settings.EMAIL_FROM,
                "to": [recipient_email],
                "subject": f"🎵 {sender_username} compartilhou uma música com você!",
                "html": html_body,
            }
            
            email = resend.Emails.send(params)
            
            logging.info(f"Música '{dto.title}' compartilhada por email de {sender_username} para {recipient_email}")
            
            return StandartOutput(
                status_code=200,
                detail=f"Música '{dto.title}' compartilhada por email com sucesso!"
            )
            
        except Exception as e:
            error_msg = f"Erro ao enviar email: {str(e)}"
            logging.error(error_msg)
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao enviar email: {str(e)}"
            )
    
    @staticmethod
    async def send_profile_share(
        dto: ShareProfileRequest, 
        sender_username: str, 
        sender_favorite_genre: str, 
        sender_profile_picture: str = None
    ) -> StandartOutput:
        
        try:
            if not Settings.RESEND_API_KEY:
                raise HTTPException(
                    status_code=500,
                    detail="Resend API Key não configurada"
                )
            
            profile_pic_html = ""
            if sender_profile_picture:
                profile_pic_html = f"""
                <div style="text-align: center; margin: 20px 0;">
                    <img src="{sender_profile_picture}" 
                         alt="Foto de perfil" 
                         style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 4px solid #667eea;">
                </div>
                """
            
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center; color: white;">
                        <h1>👤 Convite para Conectar!</h1>
                    </div>
                    
                    <div style="padding: 20px; background-color: #f9f9f9;">
                        <p style="font-size: 16px; color: #333;">
                            Olá! <strong>{sender_username}</strong> quer conectar com você no Rhythmate:
                        </p>
                        
                        {profile_pic_html}
                        
                        <div style="background-color: white; border-left: 4px solid #667eea; padding: 20px; margin: 20px 0; border-radius: 8px;">
                            <h2 style="margin: 0 0 10px 0; color: #667eea;">👤 {sender_username}</h2>
                            <p style="margin: 5px 0; color: #666;"><strong>Gênero Favorito:</strong> {sender_favorite_genre}</p>
                        </div>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{Settings.FRONTEND_URL}" 
                               style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                      color: white; padding: 15px 40px; text-decoration: none; border-radius: 25px; 
                                      font-weight: bold; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);">
                                Acessar Rhythmate
                            </a>
                        </div>
                        
                        <div style="background-color: #f0f4ff; padding: 15px; border-radius: 8px; margin: 20px 0;">
                            <p style="margin: 0; color: #555;">
                                💡 <strong>Dica:</strong> Crie sua conta e descubra músicas incríveis baseadas nos seus gostos!
                            </p>
                        </div>
                        
                        <p style="color: #888; font-size: 12px; text-align: center; margin-top: 30px;">
                            Este convite foi enviado através do Rhythmate
                        </p>
                    </div>
                </body>
            </html>
            """
            
            params = {
                "from": Settings.EMAIL_FROM,
                "to": [dto.recipient_email],
                "subject": f"👤 {sender_username} quer conectar com você no Rhythmate!",
                "html": html_body,
            }
            
            email = resend.Emails.send(params)
            
            logging.info(f"Perfil de '{sender_username}' compartilhado por email para {dto.recipient_email}")
            
            return StandartOutput(
                status_code=200,
                detail=f"Seu perfil foi compartilhado com {dto.recipient_email} com sucesso!"
            )
            
        except Exception as e:
            error_msg = f"Erro ao enviar email: {str(e)}"
            logging.error(error_msg)
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao enviar email: {str(e)}"
            )
