Rails.application.routes.draw do
  devise_for :users
  devise_for :admin_users, ActiveAdmin::Devise.config
  ActiveAdmin.routes(self)
resources :home
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html


get '/:id' => "shortener/shortened_urls#show"


root to: 'home#index'

end
