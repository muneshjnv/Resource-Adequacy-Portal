import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { environment } from '../../../environments/environment';
import { AuthenticationService } from '../../core/services/auth.service';
import { AuthfakeauthenticationService } from '../../core/services/authfake.service';
import { first } from 'rxjs/operators';
import { ToastService } from './toast-service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  loading: boolean = false;
  siteKey: string = '6Lfu97YqAAAAAE-jvR39ZWdbGYegEzV3CGF76Z0m';
  captchaResolved: boolean = false;
  captchaToken: string | null = null;
  loginForm!: UntypedFormGroup;
  submitted = false;
  fieldTextType!: boolean;
  error = '';
  returnUrl!: string;
  year: number = new Date().getFullYear();

  constructor(
    private formBuilder: UntypedFormBuilder,
    private authenticationService: AuthenticationService,
    private router: Router,
    private authFackservice: AuthfakeauthenticationService,
    private route: ActivatedRoute,
    public toastService: ToastService
  ) {
    if (this.authenticationService.currentUserValue) {
      this.router.navigate(['/']);
    }
  }

  ngOnInit(): void {
    if (localStorage.getItem('currentUser')) {
      this.router.navigate(['/']);
    }

    this.loginForm = this.formBuilder.group({
      email: ['', [Validators.required]],
      password: ['', [Validators.required]],
    });

    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
  }

  get f() { return this.loginForm.controls; }

  onCaptchaResolved(token: string): void {
    this.captchaResolved = true;
    this.captchaToken = token;
  }

  // Helper function to generate UUID for device_id
  generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = (Math.random() * 16) | 0;
      const v = c === 'x' ? r : (r & 0x3) | 0x8;
      return v.toString(16);
    });
  }

  onSubmit() {
    if (!localStorage.getItem('device_id')) {
      localStorage.setItem('device_id', this.generateUUID());
    }

    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      this.error = 'Please enter username and password.';
      return;
    }

    if (!this.captchaResolved || !this.captchaToken) {
      this.error = 'Please complete the CAPTCHA before logging in.';
      this.toastService.show('Please complete the CAPTCHA before logging in.', { classname: 'bg-warning text-white', delay: 4000 });
      return;
    }

    const device_id = localStorage.getItem('device_id');
    this.loading = true;
    this.submitted = true;

    // ✅ Remove client-side AES encryption — rely on HTTPS
    const rawPassword = this.f['password'].value;

    // Send raw password securely via HTTPS
    this.authenticationService
      .login(this.f['email'].value, rawPassword, this.captchaToken, device_id)
      .subscribe(
        (data: any) => {
          this.loading = false;
          this.router.navigate(['/']);
        },
        (error) => {
          this.loading = false;
          this.error = error?.message || 'Login failed';
        }
      );
  }

  toggleFieldTextType() {
    this.fieldTextType = !this.fieldTextType;
  }
}
