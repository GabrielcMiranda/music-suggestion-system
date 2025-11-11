import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { MusicRecommendation } from '../../modules/music/pages/recommendation/recommendation';

@Injectable({
  providedIn: 'root'
})
export class MusicService {
  
  constructor(
    private api: ApiService
  ) { }

  generateRecommendation(musicInput: string) {
    return this.api.post<{ recommendations: MusicRecommendation[] }>('my-musics/recommend', { music_input: musicInput    });
  }
}
