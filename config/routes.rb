Rails.application.routes.draw do

  devise_for :users
  devise_for :admin_users, ActiveAdmin::Devise.config
  ActiveAdmin.routes(self)



  resources :companies

  get 'dashboard/show'

  
  resources :owners do 
    resources :home do 
    end
  end



  resources :home do 
    member do
     put "select", to: "home#select"
    end
   end

resources :dashboard


get '/:id' => "shortener/shortened_urls#show"


  root to: "owners#index"

end
