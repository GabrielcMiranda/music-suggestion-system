import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { MusicRecommendation } from '../recommendation/recommendation';
import { MusicService } from '../../../../core/services/music.service';
import { AuthService } from '../../../../core/services/auth.service';
import { ShareService } from '../../../../core/services/share.service';

export interface recommendationHistory {
  recommendationId : number;
  songInput: string;
  songs: MusicRecommendation[];
}

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './history.html',
  styleUrl: './history.scss'
})

export class History implements OnInit {
  historyData: recommendationHistory[] = [];
  isLoading = false;
  errorMessage = '';
  expandedRecommendations: Set<number> = new Set();
  
  sharingMusic: MusicRecommendation | null = null;
  shareEmail = '';
  isSharing = false;
  shareErrorMessage = '';
  shareSuccessMessage = '';

  constructor(
    private router: Router,
    private authService: AuthService,
    private musicService: MusicService,
    private shareService: ShareService
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
  
  openShareModal(music: MusicRecommendation): void {
    this.sharingMusic = music;
    this.shareEmail = '';
    this.shareErrorMessage = '';
    this.shareSuccessMessage = '';
  }
  
  closeShareModal(): void {
    this.sharingMusic = null;
    this.shareEmail = '';
    this.shareErrorMessage = '';
    this.shareSuccessMessage = '';
  }
  
  shareMusic(): void {
    if (!this.shareEmail.trim()) {
      this.shareErrorMessage = 'Por favor, insira um email';
      return;
    }
    
    if (!this.sharingMusic) {
      return;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(this.shareEmail)) {
      this.shareErrorMessage = 'Por favor, insira um email válido';
      return;
    }
    
    this.isSharing = true;
    this.shareErrorMessage = '';
    this.shareSuccessMessage = '';
    
    this.shareService.shareSong(this.sharingMusic, this.shareEmail).subscribe({
      next: () => {
        this.shareSuccessMessage = 'Música compartilhada com sucesso!';
        this.isSharing = false;
        
        setTimeout(() => {
          this.closeShareModal();
        }, 2000);
      },
      error: (error) => {
        this.shareErrorMessage = error.error?.detail || 'Erro ao compartilhar música';
        this.isSharing = false;
      }
    });
  }
}
