import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../../../core/services/auth.service';
import { MusicService } from '../../../../core/services/music.service';

export interface MusicRecommendation {
  title: string;
  artist: string;
  genre: string;
  album: string;
}

@Component({
  selector: 'app-recommendation',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './recommendation.html',
  styleUrl: './recommendation.scss'
})
export class Recommendation {
  musicInput = '';
  recommendations: MusicRecommendation[] = [];
  errorMessage = '';
  isLoading = false;
  hasSearched = false;

  constructor(
    private router: Router,
    private authService: AuthService,
    private musicService: MusicService
  ) {}

  onSubmit() {
    if (!this.musicInput.trim()) {
      this.errorMessage = 'Por favor, digite o nome de uma música';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.hasSearched = true;

    this.musicService.generateRecommendation(this.musicInput).subscribe({
      next: (response) => {
        this.recommendations = response.recommendations;
        this.isLoading = false;
      },
      error: (error) => {
        this.errorMessage = error.error?.detail || 'Erro ao buscar recomendações';
        this.recommendations = [];
        this.isLoading = false;
      }
    });
  }

  logout() {
    this.authService.removeToken();
    this.router.navigate(['/auth/login']);
  }
}
