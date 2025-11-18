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
}