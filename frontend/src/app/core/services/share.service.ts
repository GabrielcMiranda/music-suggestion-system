import { Injectable } from '@angular/core';
import { MusicRecommendation } from '../../modules/music/pages/recommendation/recommendation';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root'
})

export class ShareService {

  constructor(
    private api: ApiService
  ){ }
  
  shareSong(share_request: MusicRecommendation, recipientEmail: string) { 
    return this.api.post<{status_code: number, detail: string}>(`share/song?recipient_email=${recipientEmail}`, share_request);
  }

  shareProfile(shareProfileRequest: {recipient_email: string, message?: string}) {
    return this.api.post<{status_code: number, detail: string}>('share/profile', { recipient_email: shareProfileRequest.recipient_email, message: shareProfileRequest.message });
  }
}