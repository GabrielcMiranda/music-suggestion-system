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
    return this.api.post<{ recommendations: MusicRecommendation[] }>('my-musics/recommend', { music_input: musicInput });
  }

  getMusicHistory(page: number = 1, pageSize: number = 10){
    return this.api.get<{ 
      user_musics: recommendationHistory[], 
      total: number, 
      page: number, 
      page_size: number, 
      has_more: boolean 
    }>(`my-musics?page=${page}&page_size=${pageSize}`);
  }

  getMusicStats(filter_by: string){
    return this.api.get<{ total_recommendations: number, most_requested_genre: string }>(`my-musics/stats?by=${filter_by}`);
  }
}
