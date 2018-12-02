class EngineersController < InheritedResources::Base

  before_action :authenticate_user!


def index
  @q = Engineer.where(user_id: current_user.id).ransack(params[:q])
  @engineers = @q.result.includes(:company).page(params[:page])


end


def new
  @engineer = Engineer.new
  @companies = Company.where("user_id = ?", current_user.id).order('name ASC').map { |i| [i.name, i.id]}
end

def create
  @engineer = Engineer.new(engineer_params)

  @engineer.company_id = params[:company_id]
  @engineer.user_id = current_user.id

  if @engineer.save
    redirect_to root_path
  else
    render 'new'
  end
  
end




def edit
  @engineer = Engineer.find(params[:id])    
  @companies = Company.all.order('name ASC').map { |i| [i.name, i.id]}
end


  private

    def engineer_params
      params.require(:engineer).permit(:firstname, :lastname, :email, :company_id, :user_id)
    end
end
