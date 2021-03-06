import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http'
import { FormsModule } from '@angular/forms';
import { ToastyModule } from 'ng2-toasty';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { NavbarTopComponent } from './navbar-top/navbar-top.component';
import { SiderbarLeftComponent } from './siderbar-left/siderbar-left.component';
import { CreateHealthcareTestComponent } from './create-healthcare-test/create-healthcare-test.component';
import { RatingComponent } from './rating/rating.component';

import { AuthGuard, DoctorGuard } from './http.service'
import { AuthService } from './http.service';
import { MyWalletComponent } from './my-wallet/my-wallet.component';
import { HealthCareRecordComponent } from './health-care-record/health-care-record.component';
import { DoctorRatingComponent } from './doctor-rating/doctor-rating.component';
import { HistoryTransactionComponent } from './history-transaction/history-transaction.component';
import { ModalModule } from "ng2-modal";

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    DashboardComponent,
    NavbarTopComponent,
    SiderbarLeftComponent,
    MyWalletComponent,
    HealthCareRecordComponent,
    DoctorRatingComponent,
    HistoryTransactionComponent,
    CreateHealthcareTestComponent,
    RatingComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ModalModule,
    ToastyModule.forRoot(),
  ],
  providers: [AuthGuard,AuthService,DoctorGuard],
  bootstrap: [AppComponent]
})
export class AppModule { }
