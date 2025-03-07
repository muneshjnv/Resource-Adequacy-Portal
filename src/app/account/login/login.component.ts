import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

// Login Auth
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

/**
 * Login Component
 */
export class LoginComponent implements OnInit {


  loading: boolean= false;
  

  siteKey: string = '6Lfu97YqAAAAAE-jvR39ZWdbGYegEzV3CGF76Z0m';

  captchaResolved: boolean = false;
  captchaToken: string | null = null;

  // Login Form
  loginForm!: UntypedFormGroup;
  submitted = false;
  fieldTextType!: boolean;
  error = '';
  returnUrl!: string;
  // set the current year
  year: number = new Date().getFullYear();

  constructor(private formBuilder: UntypedFormBuilder,private authenticationService: AuthenticationService,private router: Router,
    private authFackservice: AuthfakeauthenticationService,private route: ActivatedRoute, public toastService: ToastService, ) {
      // redirect to home if already logged in
      if (this.authenticationService.currentUserValue) {
        this.router.navigate(['/']);
      }
     }

  ngOnInit(): void {
    if(localStorage.getItem('currentUser')) {
      this.router.navigate(['/']);
    }
    /**
     * Form Validatyion
     */
     this.loginForm = this.formBuilder.group({
      email: ['', [Validators.required]],
      password: ['', [Validators.required]],
    });
    // get return url from route parameters or default to '/'
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
  }

  // convenience getter for easy access to form fields
  get f() { return this.loginForm.controls; }

  onCaptchaResolved(token: string): void {
    this.captchaResolved = true;
    this.captchaToken = token;
    // console.log(`Resolved captcha with response: ${token}`);
  }

  /**
   * Form submit
   */

  // Helper function to generate a UUID for device_id
generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}




   onSubmit() {

    // Example using JavaScript
    if (!localStorage.getItem('device_id')) {
      localStorage.setItem('device_id', this.generateUUID());
    }

    const device_id = localStorage.getItem('device_id');
    this.loading = true;
    this.submitted = true;
     // Login Api
     this.authenticationService.login(this.f['email'].value, this.f['password'].value, this.captchaToken as string, device_id).subscribe((data:any) => {   
      this.loading = false;   
      // if(data.status == 'success'){
        
        // localStorage.setItem('toast', 'true');
        // localStorage.setItem('currentUser', JSON.stringify(data.data));
        // localStorage.setItem('token', data.token);
        this.router.navigate(['/']);

      // }
    });

    

    // stop here if form is invalid
    // if (this.loginForm.invalid) {
    //   return;
    // } else {
    //   if (environment.defaultauth === 'firebase') {
    //     this.authenticationService.login(this.f['email'].value, this.f['password'].value).then((res: any) => {
    //       this.router.navigate(['/']);
    //     })
    //       .catch(error => {
    //         this.error = error ? error : '';
    //       });
    //   } else {
    //     this.authFackservice.login(this.f['email'].value, this.f['password'].value).pipe(first()).subscribe(data => {
    //           this.router.navigate(['/']);
    //         },
    //         error => {
    //           this.error = error ? error : '';
    //         });
    //   }
    // }
  }

  /**
   * Password Hide/Show
   */
   toggleFieldTextType() {
    this.fieldTextType = !this.fieldTextType;
  }

}
