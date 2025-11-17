import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { MusicRecommendation } from '../recommendation/recommendation';
import { MusicService } from '../../../../core/services/music.service';
import { AuthService } from '../../../../core/services/auth.service';

export interface recommendationHistory {
  recommendationId : number;
  songInput: string;
  songs: MusicRecommendation[];
}

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './history.html',
  styleUrl: './history.scss'
})

export class History implements OnInit {
  historyData: recommendationHistory[] = [];
  isLoading = false;
  errorMessage = '';
  expandedRecommendations: Set<number> = new Set();

  constructor(
    private router: Router,
    private authService: AuthService,
    private musicService: MusicService
  ) {}

  ngOnInit(): void {
    this.loadHistory();
  }

  loadHistory(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.musicService.getMusicHistory().subscribe({
      next: (response: any) => {
        const userMusics = response.user_musics || response;
        
        this.historyData = userMusics.map((item: any) => ({
          recommendationId: item.recommendation_id,
          songInput: item.song_input,
          songs: item.musics
        }));
        
        this.isLoading = false;
      },
      error: (error) => {
        this.errorMessage = error.error?.detail || 'Erro ao carregar histórico';
        this.isLoading = false;
      }
    });
  }

  toggleRecommendation(id: number): void {
    if (this.expandedRecommendations.has(id)) {
      this.expandedRecommendations.delete(id);
    } else {
      this.expandedRecommendations.add(id);
    }
  }

  isExpanded(id: number): boolean {
    return this.expandedRecommendations.has(id);
  }

  logout(): void {
    this.authService.removeToken();
    this.router.navigate(['/auth/login']);
  }
}
