import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { MusicService } from '../../../../core/services/music.service';
import { AuthService } from '../../../../core/services/auth.service';
import { ShareService } from '../../../../core/services/share.service';

export interface StatsItem {
  name: string;
  count: number;
}

export interface TopMusic {
  title: string;
  artist: string;
  genre: string;
  album: string;
  count: number;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})

export class Dashboard implements OnInit, AfterViewInit {
  @ViewChild('chartCanvas', { static: false }) chartCanvas!: ElementRef<HTMLCanvasElement>;
  
  filterBy: 'artist' | 'genre' = 'artist';
  totalRecommendations = 0;
  stats: StatsItem[] = [];
  topMusics: TopMusic[] = [];
  isLoading = false;
  errorMessage = '';
  searchTerm = '';
  private ctx: CanvasRenderingContext2D | null = null;
  Math = Math;
  
  sharingMusic: TopMusic | null = null;
  shareEmail = '';
  isSharing = false;
  shareErrorMessage = '';
  shareSuccessMessage = ''; 

  constructor(
    private musicService: MusicService,
    private authService: AuthService,
    private router: Router,
    private shareService: ShareService
  ) {}

  ngOnInit(): void {
    this.loadStats();
  }

  ngAfterViewInit(): void {
    
  }

  loadStats(): void {
    this.isLoading = true;
    this.errorMessage = '';
    
    this.musicService.getMusicStats(this.filterBy).subscribe({
      next: (response: any) => {
        this.totalRecommendations = response.total_recommendations;
        
        this.stats = Object.entries(response.stats)
          .map(([name, count]) => ({
            name,
            count: count as number
          }))
          .sort((a, b) => b.count - a.count);
        
        this.topMusics = response.top_musics || [];
        
        this.isLoading = false;
        
     
        setTimeout(() => this.drawChart(), 200);
      },
      error: (error) => {
        this.errorMessage = error.error?.detail || 'Erro ao carregar estatísticas';
        this.isLoading = false;
      }
    });
  }

  drawChart(): void {
    if (!this.chartCanvas || this.filteredStats.length === 0) {
      console.log('Canvas ou dados não disponíveis');
      return;
    }

    const canvas = this.chartCanvas.nativeElement;
    const ctx = canvas.getContext('2d');
    
    if (!ctx) {
      console.error('Não foi possível obter o contexto 2D do canvas');
      return;
    }
    
    this.ctx = ctx;
    

    const bgGradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
    bgGradient.addColorStop(0, '#111827');
    bgGradient.addColorStop(1, '#1F2937');
    ctx.fillStyle = bgGradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    const data = this.filteredStats;
    const maxValue = Math.max(...data.map(d => d.count));
    const paddingLeft = 60;
    const paddingRight = 60;
    const paddingTop = 80;
    const paddingBottom = 100;
    const chartWidth = canvas.width - paddingLeft - paddingRight;
    const chartHeight = canvas.height - paddingTop - paddingBottom;
    const barWidth = Math.min((chartWidth - (data.length - 1) * 20) / data.length, 80); 
    const spacing = 20;
    const totalBarSpace = (barWidth * data.length) + (spacing * (data.length - 1));
    const startX = paddingLeft + 10;
    
    
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 1;
    ctx.setLineDash([5, 5]); 
    for (let i = 0; i <= 5; i++) {
      const y = paddingTop + (chartHeight / 5) * i;
      ctx.beginPath();
      ctx.moveTo(paddingLeft + 10, y);
      ctx.lineTo(canvas.width - paddingRight, y);
      ctx.stroke();
    }
    ctx.setLineDash([]); 
    
 
    data.forEach((item, index) => {
      const barHeight = (item.count / maxValue) * chartHeight;
      const x = startX + index * (barWidth + spacing);
      const y = paddingTop + chartHeight - barHeight;
      
      
      ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
      ctx.shadowBlur = 15;
      ctx.shadowOffsetX = 0;
      ctx.shadowOffsetY = 5;
      
      
      const gradient = ctx.createLinearGradient(x, y, x, paddingTop + chartHeight);
      if (index === 0) {
        
        gradient.addColorStop(0, '#FCD34D');
        gradient.addColorStop(0.5, '#F59E0B');
        gradient.addColorStop(1, '#D97706');
      } else if (index === 1) {
        
        gradient.addColorStop(0, '#E5E7EB');
        gradient.addColorStop(0.5, '#9CA3AF');
        gradient.addColorStop(1, '#6B7280');
      } else if (index === 2) {
        
        gradient.addColorStop(0, '#FCA5A5');
        gradient.addColorStop(0.5, '#EF4444');
        gradient.addColorStop(1, '#DC2626');
      } else {
       
        gradient.addColorStop(0, '#A855F7');
        gradient.addColorStop(0.5, '#9333EA');
        gradient.addColorStop(1, '#7C3AED');
      }
      
     
      ctx.fillStyle = gradient;
      this.roundRect(ctx, x, y, barWidth, barHeight, 10);
      ctx.fill();
      
    
      ctx.shadowColor = 'transparent';
      ctx.shadowBlur = 0;
      ctx.shadowOffsetX = 0;
      ctx.shadowOffsetY = 0;
      
  
      const highlightGradient = ctx.createLinearGradient(x, y, x, y + 30);
      highlightGradient.addColorStop(0, 'rgba(255, 255, 255, 0.4)');
      highlightGradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
      ctx.fillStyle = highlightGradient;
      this.roundRect(ctx, x, y, barWidth, Math.min(30, barHeight), 10);
      ctx.fill();
      
      
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
      ctx.lineWidth = 2;
      this.roundRect(ctx, x, y, barWidth, barHeight, 10);
      ctx.stroke();
      
     
      const valueText = item.count.toString();
      ctx.font = 'bold 18px Inter, Arial, sans-serif';
      ctx.textAlign = 'center';
      const textMetrics = ctx.measureText(valueText);
      const textWidth = textMetrics.width;
      const textHeight = 24;
      const badgeX = x + barWidth / 2 - textWidth / 2 - 8;
      const badgeY = y - 35;
      
      
      ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
      ctx.beginPath();
      ctx.roundRect(badgeX, badgeY, textWidth + 16, textHeight, 8);
      ctx.fill();
      
    
      ctx.fillStyle = '#FFFFFF';
      ctx.fillText(valueText, x + barWidth / 2, y - 15);
      
      
      ctx.font = 'bold 13px Inter, Arial, sans-serif';
      ctx.fillStyle = '#F3F4F6';
      ctx.textAlign = 'center';
      ctx.save();
      ctx.translate(x + barWidth / 2, paddingTop + chartHeight + 25);
      
      const maxCharsPerLine = 12;
      const words = item.name.split(' ');
      const lines: string[] = [];
      let currentLine = '';
      
      for (const word of words) {
        const testLine = currentLine ? currentLine + ' ' + word : word;
        if (testLine.length <= maxCharsPerLine) {
          currentLine = testLine;
        } else {
          if (currentLine) lines.push(currentLine);
          currentLine = word;
        }
      }
      if (currentLine) lines.push(currentLine);
      
      if (lines.length > 2) {
        lines[1] = lines[1].substring(0, maxCharsPerLine - 3) + '...';
        lines.length = 2;
      }
      
      lines.forEach((line, lineIndex) => {
        ctx.fillText(line, 0, lineIndex * 16);
      });
      
      ctx.font = 'bold 11px Inter, Arial, sans-serif';
      ctx.fillStyle = '#9CA3AF';
      ctx.fillText(`#${index + 1}`, 0, lines.length * 16 + 6);
      
      ctx.restore();
    });
    
    const numDivisions = maxValue <= 5 ? maxValue : 5;
    const step = maxValue / numDivisions;
    
    for (let i = 0; i <= numDivisions; i++) {
      const y = paddingTop + (chartHeight / numDivisions) * i;
      const value = Math.round(maxValue - step * i);
      
      if (i === 0 || value !== Math.round(maxValue - step * (i - 1))) {
        ctx.fillStyle = '#D1D5DB';
        ctx.font = 'bold 14px Inter, Arial, sans-serif';
        ctx.textAlign = 'right';
        ctx.fillText(value.toString(), paddingLeft - 5, y + 5);
      }
    }
  }

  
  private roundRect(ctx: CanvasRenderingContext2D, x: number, y: number, width: number, height: number, radius: number): void {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    ctx.lineTo(x + radius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
  }

  onFilterChange(): void {
    this.searchTerm = ''; 
    this.loadStats();
  }

  onSearchChange(): void {
    this.drawChart();
  }

  get filteredStats(): StatsItem[] {
    if (!this.searchTerm.trim()) {
      return this.stats;
    }
    
    const search = this.searchTerm.toLowerCase();
    return this.stats.filter(stat => 
      stat.name.toLowerCase().includes(search)
    );
  }

  get filterLabel(): string {
    return this.filterBy === 'artist' ? 'Artista' : 'Gênero';
  }

  logout(): void {
    localStorage.removeItem('access_token');
    this.router.navigate(['/login']);
  }
  
  openShareModal(music: TopMusic): void {
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
