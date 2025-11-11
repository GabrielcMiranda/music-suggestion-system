import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../../../core/services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './register.html',
  styleUrl: './register.scss'
})
export class Register {
  registerRequest ={
    username: '',
    email: '',
    password: '',
    matchPassword: ''
  }

  errorMessage: string = '';
  isLoading: boolean = false;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  onSubmit() {
    if (!this.registerRequest.username || !this.registerRequest.email || !this.registerRequest.password || !this.registerRequest.matchPassword) {
      this.errorMessage = 'Por favor, preencha todos os campos';
      return;
    }

    if (this.registerRequest.password !== this.registerRequest.matchPassword) {
      this.errorMessage = 'As senhas não coincidem';
      return;
    }
    const registerData = {
      username: this.registerRequest.username,
      email: this.registerRequest.email,
      password: this.registerRequest.password
    };

    this.isLoading = true;
    this.errorMessage = '';

    this.authService.register(registerData).subscribe({
      next: (response) => {
        this.isLoading = false;
        this.router.navigate(['/music/recommendation']);
      },
      error: (error) => {
        this.isLoading = false;
        this.errorMessage = error.error?.detail || 'Erro ao registrar. Tente novamente.';
        console.error('Erro completo:', error);
      }
    });
  }
}
