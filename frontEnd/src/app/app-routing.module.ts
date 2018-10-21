import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { MyWalletComponent } from './my-wallet/my-wallet.component';
import { HealthCareRecordComponent } from './health-care-record/health-care-record.component';
import { DoctorRatingComponent } from './doctor-rating/doctor-rating.component';
import { HistoryTransactionComponent } from './history-transaction/history-transaction.component';

import { AuthGuard } from './http.service';
const routes: Routes = [

  	{
	    path: '',
	    redirectTo: '/dashboard',
	    pathMatch: 'full',
  	},
	{
		path :'dashboard',
		component: DashboardComponent,
		canActivate:[AuthGuard],
	},
	{
		path :'wallet',
		component: MyWalletComponent,
		canActivate:[AuthGuard],
	},
	{
		path :'health-care-record',
		component: HealthCareRecordComponent,
		canActivate:[AuthGuard],
	},
	{
		path :'doctor-rating',
		component: DoctorRatingComponent,
		canActivate:[AuthGuard],
	},
	{
		path :'history-transaction',
		component: HistoryTransactionComponent,
		canActivate:[AuthGuard],
	},
	{
		path :'login',
		component: LoginComponent
	},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
