import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { MusicRecommendation } from '../../modules/music/pages/recommendation/recommendation';
import { recommendationHistory } from '../../modules/music/pages/history/history';

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

  getMusicHistory(){
    return this.api.get<recommendationHistory[]>('my-musics');
  }

  getMusicStats(filter_by: string){
    return this.api.get<{ total_recommendations: number, most_requested_genre: string }>(`my-musics/stats?by=${filter_by}`);
  }
}
