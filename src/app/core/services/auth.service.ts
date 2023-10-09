import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { throwError, BehaviorSubject, Observable } from 'rxjs';
import {catchError, map, mergeMap} from 'rxjs/operators'
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { JwtHelperService } from '@auth0/angular-jwt';
import swal from 'sweetalert2';
import { api_url } from '../helpers/urlentry';
import { ToastService } from 'src/app/account/login/toast-service';

@Injectable({
  providedIn: 'root'
})





export class AuthenticationService {
  

  url = api_url;
  constructor(public http: HttpClient, public toastService: ToastService ) {
    this.currentUserSubject = new BehaviorSubject<any>(JSON.parse(localStorage.getItem('currentUser')!));
        this.currentUser = this.currentUserSubject.asObservable();
   }

    // Handle authentication errors
    private currentUserSubject: BehaviorSubject<any>;
    public currentUser: Observable<any>;  

    login(username: string, password: string) {

 
      // console.log(username);


      return this.http.post<any>(this.url + '/login', { username, password })
          .pipe(map(user => {
              // store user details and jwt token in local storage to keep user logged in between page refreshes
            //   console.log(user);
              if('error' in user) {
                this.toastService.show(user['error'], { classname: 'bg-danger text-white', delay: 5000 });
              }
              else {

                localStorage.setItem('currentUser', JSON.stringify(user));
                // this.toastService.show(user['error'], { classname: 'bg-danger text-white', delay: 5000 });
                this.currentUserSubject.next(user);
                return user;
              }
              
          }));
  }

  public get currentUserValue(): any {
    return this.currentUserSubject.value;
}

  logout() {
      // remove user from local storage to log user out
      localStorage.removeItem('currentUser');
      this.currentUserSubject.next(null);
      // this.currentUserSubject = null;
  }

  isLoggedIn() {
    return this.http.get<any>(this.url + '/protected')
  }


}




